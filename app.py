import os
from flask import Flask, render_template, request
from crewai import Agent, Task, Crew
from time import time
# Make sure your OPENAI_API_KEY is set in the environment
# Scenario - Automatic email responder
app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    response = None
    latency = None
    customer_message = ""
    planner_result = None

    print("🔥 NEW CODE RUNNING")

    if request.method == 'POST':
        DEFAULT_MESSAGE = """Subject: My order arrived damaged

        Hi team, my blender arrived with a cracked jar and the motor smells burnt.
        Order #A12345. I need this for an event on Friday—can you help?
        """

        customer_message = request.form.get('message', DEFAULT_MESSAGE)
        planner_result = None
        latency = None   

        planner = Agent(
            role="Support Planner",
            goal="Choose the best support strategy for the customer's issue.",
            backstory="You are concise and decisive. You output a numbered plan only.",
            verbose=False
        )

        writer = Agent(
            role="Support Writer",
            goal="Write a friendly, empathetic 4-line reply that follows the plan.",
            backstory="You speak like a helpful human. Keep it simple and professional.",
            verbose=False
        )

        plan_task = Task(
            description="""
            Read the customer's message below. Produce a 3-step support plan:
            1) Classify severity (low/medium/high)
            2) Decide actions (apology, replacement/refund, expedited shipping, ask for photos, etc.)
            3) Key details to include (order number acknowledgment, timing)

            CUSTOMER MESSAGE:
            {customer_message}
            """,
            expected_output="A numbered 3-step plan, one line per step.",
            agent=planner
        )

        reply_task = Task(
            description="""
            Using the planner's output, write a friendly customer reply:
            - Exactly 4 short lines (no more, no less)
            - Include apology (if needed), concrete next steps, and timing
            - Reference their order number if present
            - Avoid jargon and keep it reassuring
            """,
            expected_output="A 4-line email-style reply.",
            agent=writer
        )
        """
        crew = Crew(
            agents=[planner, writer],
            tasks=[plan_task, reply_task],
            process="sequential"
        )

        response = crew.kickoff()

    return render_template('index.html', response=response, message=customer_message)
    """
        start_time = time()

        # Run planner only
        planner_crew = Crew(
            agents=[planner],
            tasks=[plan_task],
            process="sequential"
        )
        plan_output = planner_crew.kickoff()

        # Run writer using planner output
        reply_task.context = str(plan_output)

        writer_crew = Crew(
            agents=[writer],
            tasks=[reply_task],
            process="sequential"
        )
        final_response = writer_crew.kickoff()

        end_time = time()

        response = final_response
        planner_result = plan_output
        latency = round(end_time - start_time, 2)

    return render_template('index.html',response=response,planner_result=planner_result,latency=latency,message=customer_message)

if __name__ == '__main__':
    app.run(debug=True)