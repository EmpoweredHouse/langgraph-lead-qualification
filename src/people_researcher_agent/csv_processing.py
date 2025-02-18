import csv
import asyncio

from dotenv import load_dotenv, find_dotenv
dotenv_path = find_dotenv(usecwd=True)
load_dotenv(dotenv_path)

from people_researcher_agent.graph import graph
from people_researcher_agent.state import InputState, DEFAULT_EXTRACTION_SCHEMA


# Limit the number of concurrent tasks (e.g., max 10 at a time)
semaphore = asyncio.Semaphore(5)


async def process_person(row: dict) -> dict:
    person = {
        "name": row.get("first_name") + " " + row.get("last_name"),
        "company": row.get("company_name"),
        "linkedin": row.get("linked_in_url"),
        "email": row.get("personal_email"),
        "role": row.get("business_job_title"),
    }

    initial_state = InputState(
        person=person
    )

    async with semaphore:
        result = await graph.ainvoke(initial_state)
        return result


async def main(input_filename: str, output_filename: str):
    tasks = []
    original_rows = []

    # Read original CSV rows
    with open(input_filename, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            original_rows.append(row)
            tasks.append(process_person(row))
    print(f"Processing {len(tasks)} rows...")

    # Process rows concurrently
    results = await asyncio.gather(*tasks, return_exceptions=True)
    print(results)

    original_headers = list(original_rows[0].keys()) if original_rows else []
    new_headers = DEFAULT_EXTRACTION_SCHEMA['required']
    combined_headers = original_headers + new_headers
    dummy_result = {key: "None" for key in new_headers}

    # Write combined data to a new CSV file.
    with open(output_filename, "w", newline="", encoding="utf-8") as outfile:
        writer = csv.DictWriter(outfile, fieldnames=combined_headers)
        writer.writeheader()
        new_headers = set(new_headers)
        for row, result in zip(original_rows, results):
            if isinstance(result, Exception):
                print(f"Error processing row: {result}")
                row.update(dummy_result)
            elif not isinstance(result, dict):
                print(f"Unexpected result type: {result}")
                row.update(dummy_result)
            elif result.get('info') is not None and set(result['info'].keys()) == new_headers:
                row.update(result['info'])
            else:
                row.update(dummy_result)
            writer.writerow(row)

    print(f"Results saved to {output_filename}")


if __name__ == "__main__":
    input_file = "../../data.csv"
    output_file = "../../data_with_results.csv"
    asyncio.run(main(input_file, output_file))
