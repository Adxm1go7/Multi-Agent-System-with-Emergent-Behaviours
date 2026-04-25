Running the React Cellular Automata website:

In terminal:
/srcReact/my-react-app/frontend> npm run dev


In 2nd terminal:
/srcReact/my-react-app/backend> uvicorn server:app --reload

To run experiments and pull graphs:
(First set parameter values inside experiments)

In terminal:
/srcReact/my-react-app/backend> python experiments.py
/srcReact/my-react-app/backend> python analyse.py
