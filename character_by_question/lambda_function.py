import json
import pg8000

# -----------------------------------
# Extract name from simple question
# -----------------------------------
def extract_name_from_question(question):
    question = question.replace("?", "").strip()
    words = question.split()

    if len(words) >= 3:
        return " ".join(words[-3:])
    else:
        return words[-1]


# -----------------------------------
# Searching character in RDS
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
    ] if fruits else "Does not own"

    cursor.close()
    conn.close()

    return result


# -----------------------------------
# Format redacted answer
# -----------------------------------
def format_character_answer(character):

    fruits = character["devil_fruits"]

    if fruits == "Does not own":
        fruits_text = "No Devil Fruit"
    else:
        fruits_text = ", ".join(
            [f"{f['name']} ({f['type']})" for f in fruits]
        )

    answer = (
        f"{character['name']} is a character from {character['sea']}. "
        f"Originally from {character['island']}, currently {character['status']}. "
        f"Affiliation: {character['affiliation']}. "
        f"Devil Fruit: {fruits_text}."
    )

    return answer


# -----------------------------------
# Lambda Handler
# -----------------------------------
def lambda_handler(event, context):

    print("EVENT RECEIVED:", event)

    try:
        body = json.loads(event["body"]) if "body" in event else event

        name = body.get("name")
        question = body.get("question")

        if name:
            result = get_character_by_name(name)

            if not result:
                return {
                    "statusCode": 404,
                    "body": json.dumps("Character not found")
                }

            return {
                "statusCode": 200,
                "body": json.dumps(result)
            }

        elif question:
            extracted_name = extract_name_from_question(question)
            result = get_character_by_name(extracted_name)

            if not result:
                return {
                    "statusCode": 404,
                    "body": json.dumps("Character not found")
                }

            formatted_answer = format_character_answer(result)

            return {
                "statusCode": 200,
                "headers": {
                    "Content-Type": "application/json"
                            },
                "body": json.dumps({
                    "answer": formatted_answer
                 })
            }

        else:
            return {
                "statusCode": 400,
                "headers": {
                    "Content-Type": "application/json"
                            },
                "body": json.dumps({
                    "answer": formatted_answer
                 })
            }

    except Exception as e:
        return {
                "statusCode": 500,
                "headers": {
                    "Content-Type": "application/json"
                            },
                "body": json.dumps({
                    "answer": formatted_answer
                 })
            }