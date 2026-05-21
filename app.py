import pandas as pd
from flask import Flask, jsonify, request, render_template_string

app = Flask(__name__)
app.json.ensure_ascii = False


def load_data():
    tables = {}
    for hw in ("hw-01", "hw-02"):
        df = pd.read_csv(f"{hw}.csv")
        df.columns = df.columns.str.strip()
        df = df.loc[:, ~df.columns.str.startswith("Unnamed")]
        df = df.rename(columns={
            "ФИ":          "name",
            "Группа":      "group_id",
            "Ссылка на MR": "mr_url",
            "Баллы":       "score",
        })
        df = df.dropna(subset=["name"])
        df = df[df["name"].str.strip() != ""]
        df["score"] = pd.to_numeric(df["score"], errors="coerce").fillna(0)
        df["group_id"] = (
            df["group_id"]
            .astype(str)
            .str.strip()
            .str.replace(r"\.0$", "", regex=True)
        )
        df["name"] = df["name"].str.strip()
        df = df.reset_index(drop=True)
        df["student_id"] = range(1, len(df) + 1)
        tables[hw] = df
    return tables


DATA = load_data()
ALL_STUDENTS = (
    pd.concat(DATA.values())[["student_id", "name", "group_id"]]
    .drop_duplicates(subset=["name"])
    .reset_index(drop=True)
)


def get_hw(hw_name):
    return DATA.get(hw_name)


def calc_mark(total_score):
    if total_score >= 50:
        return 5
    elif total_score >= 30:
        return 4
    elif total_score >= 1:
        return 3
    return 2


@app.route("/")
def index():
    return jsonify({"available_endpoints": [
        "GET /names",
        "GET /hw-01/mean_score",
        "GET /hw-02/mean_score",
        "GET /hw-01/<group_id>/mean_score",
        "GET /mean_score?hw_name=hw-01&group_id=25137",
        "GET /mark?student_id=1",
        "GET /mark?group_id=25137",
        "GET /course_table?hw_name=hw-01",
        "GET /course_table?hw_name=hw-01&group_id=25137",
    ]})


@app.route("/names")
def names():
    return jsonify({"names": ALL_STUDENTS["name"].tolist()})


@app.route("/<hw_name>/mean_score")
def hw_mean_score(hw_name):
    df = get_hw(hw_name)
    if df is None:
        return jsonify({"error": f"Домашка '{hw_name}' не найдена"}), 404
    return jsonify({"hw": hw_name, "mean_score": round(df["score"].mean(), 2)})


@app.route("/<hw_name>/<group_id>/mean_score")
def hw_group_mean_score(hw_name, group_id):
    df = get_hw(hw_name)
    if df is None:
        return jsonify({"error": f"Домашка '{hw_name}' не найдена"}), 404
    group_df = df[df["group_id"] == str(group_id)]
    if group_df.empty:
        return jsonify({"error": f"Группа '{group_id}' не найдена"}), 404
    return jsonify({"hw": hw_name, "group_id": group_id,
                    "mean_score": round(group_df["score"].mean(), 2)})


@app.route("/mean_score")
def mean_score():
    hw_name = request.args.get("hw_name")
    group_id = request.args.get("group_id")
    if not hw_name:
        return jsonify({"error": "Параметр hw_name обязателен"}), 400
    df = get_hw(hw_name)
    if df is None:
        return jsonify({"error": f"Домашка '{hw_name}' не найдена"}), 404
    if group_id:
        df = df[df["group_id"] == str(group_id)]
        if df.empty:
            return jsonify({"error": f"Группа '{group_id}' не найдена"}), 404
    return jsonify({"hw": hw_name, "group_id": group_id,
                    "mean_score": round(df["score"].mean(), 2)})


@app.route("/mark")
def mark():
    student_id = request.args.get("student_id")
    group_id = request.args.get("group_id")
    if not student_id and not group_id:
        return jsonify({"error": "Нужен student_id или group_id"}), 400

    all_df = pd.concat(DATA.values())

    if student_id:
        rows = all_df[all_df["student_id"].astype(str) == str(student_id)]
        if rows.empty:
            return jsonify({"error": f"Студент с id '{student_id}' не найден"}), 404
        total = rows["score"].sum()
        return jsonify({"student_id": student_id, "name": rows.iloc[0]["name"],
                        "total_score": total, "mark": calc_mark(total)})

    group_df = all_df[all_df["group_id"] == str(group_id)]
    if group_df.empty:
        return jsonify({"error": f"Группа '{group_id}' не найдена"}), 404
    per_student = group_df.groupby("student_id")["score"].sum().apply(calc_mark)
    return jsonify({"group_id": group_id, "mean_mark": round(per_student.mean(), 2)})


HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <title>{{ hw_name }}{% if group_id %} | группа {{ group_id }}{% endif %}</title>
  <style>
    body  { font-family: Arial, sans-serif; padding: 28px; color: #222; }
    h2    { margin-bottom: 14px; }
    table { border-collapse: collapse; width: 100%; max-width: 900px; }
    th    { background: #4a6cf7; color: #fff; padding: 10px 14px; text-align: left; }
    td    { padding: 8px 14px; border-bottom: 1px solid #ddd; }
    tr:nth-child(even) td { background: #f5f7ff; }
    tr:hover td { background: #eef0ff; }
  </style>
</head>
<body>
  <h2>{{ hw_name }}{% if group_id %} — группа {{ group_id }}{% else %} — все группы{% endif %}</h2>
  {{ table | safe }}
</body>
</html>"""


@app.route("/course_table")
def course_table():
    hw_name = request.args.get("hw_name")
    group_id = request.args.get("group_id")
    if not hw_name:
        return jsonify({"error": "Параметр hw_name обязателен"}), 400
    df = get_hw(hw_name)
    if df is None:
        return jsonify({"error": f"Домашка '{hw_name}' не найдена"}), 404
    if group_id:
        df = df[df["group_id"] == str(group_id)]
        if df.empty:
            return jsonify({"error": f"Группа '{group_id}' не найдена"}), 404
    show = df[["student_id", "name", "group_id", "score"]].rename(columns={
        "student_id": "№", "name": "ФИ", "group_id": "Группа", "score": "Баллы"
    })
    table_html = show.to_html(index=False, border=0)
    return render_template_string(HTML_TEMPLATE, hw_name=hw_name,
                                  group_id=group_id, table=table_html)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=1337, debug=True)