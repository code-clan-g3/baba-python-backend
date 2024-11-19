import logging
import time


def wait_for_run_completion(client, thread_id, run_id, sleep_time):
    while True:
        try:
            run = client.beta.threads.runs.retrieve(
                thread_id=thread_id,
                run_id=run_id,
            )
            if run.completed_at:
                elapsed_time = run.completed_at - run.created_at
                formatted_elapsed_time = time.strftime("%H:%M:%S", time.gmtime(elapsed_time))
                print(f"Run completed in {formatted_elapsed_time}")
                logging.info(f"Run completed in {formatted_elapsed_time}")

                messages = client.beta.threads.messages.list(thread_id=thread_id)
                last_message = messages.data[0]
                response = last_message.content[0].text.value
                print(f"Assistant response: {response}")
                return response
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            break
        logging.info(f"Waiting for run to complete...")
        time.sleep(sleep_time)
