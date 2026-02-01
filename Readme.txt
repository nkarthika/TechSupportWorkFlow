
This webapp shows how a muliagent system can orchesrate between agents to create an automatic response to an email or a message that
is sent from a customer. In his case there are 2 agents run sequentially. 
The first one, planner agent classifies the severity of the message(critical, medium or low), decides what will be the response or action
for this email, and include any key details in the response.
The second agent, writer agent, is asked to respond in a professional way and write only 4 lines in the response email.

Uses Flask, CrewAI(including Openai)
Export openai key into your environment so Crewai can access it automatically wihout having to call it explicitly from code.
