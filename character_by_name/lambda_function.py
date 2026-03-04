import json
import pg8000

# -----------------------------------
# Search character in RDS
# -----------------------------------
def get_character_by_name(name):

    conn = pg8000.connect(
        host="HOST HERE",
        database="DATABASE_NAME",
        user="USER HERE",
        password="USER HERE",
        port=5432
    )

    cursor = conn.cursor()

    # Partial search
    cursor.execute("""
        SELECT character_id, name, sea, island, status, affiliation
        FROM characters
        WHERE LOWER(name) LIKE LOWER(%s)
        LIMIT 1;
    """, (f"%{name}%",))

    character = cursor.fetchone()

    if not character:
        cursor.close()
        conn.close()
        return None

    character_id = character[0]

    result = {
        "name": character[1],
        "sea": character[2],
        "island": character[3],
        "status": character[4],
        "affiliation": character[5],
    }

    # Devil Fruits
    cursor.execute("""
        SELECT name, type
        FROM devil_fruits
        WHERE user_id = %s;
    """, (character_id,))

    fruits = cursor.fetchall()

    result["devil_fruits"] = [
        {"name": f[0], "type": f[1]}
        for f in fruits
    ] if fruits else []

    cursor.close()
    conn.close()

    return result


# -----------------------------------
# Format type JSON
# -----------------------------------
def format_character_answer(character):

    fruits_text = ""

    if character["devil_fruits"]:
        for fruit in character["devil_fruits"]:
            fruits_text += f'        {{ "name": "{fruit["name"]}", "type": "{fruit["type"]}" }}\n'
    else:
        fruits_text = '        "None"\n'

    formatted = f"""
{{
    "name": "{character['name']}",
    "sea": "{character['sea']}",
    "island": "{character['island']}",
    "status": "{character['status']}",
    "affiliation": "{character['affiliation']}",
    "devil_fruits": [
{fruits_text}    ]
}}
"""

    return formatted.strip()


# -----------------------------------
# Lambda Handler
# -----------------------------------
def lambda_handler(event, context):

    print("EVENT RECEIVED:", event)

    body = json.loads(event["body"]) if "body" in event else event
    name = body.get("name")

    if not name:
        return {
            "statusCode": 400,
            "body": json.dumps("Missing 'name'")
        }

    result = get_character_by_name(name)

    if not result:
        return {
            "statusCode": 404,
            "body": json.dumps("Character not found")
        }

    answer_output = format_character_answer(result)

    return {
        "statusCode": 200,
        "body": json.dumps({"result": answer_output})
    }
