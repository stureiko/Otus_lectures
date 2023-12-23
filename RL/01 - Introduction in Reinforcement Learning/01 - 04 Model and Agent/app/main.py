from fastapi import FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import HTMLResponse
from fastapi.responses import JSONResponse
from jinja2 import Environment, PackageLoader, select_autoescape

from app.continuous_states_continuous_actions import ContinuousStatesContinuousActions
from app.continuous_states_discrete_actions import ContinuousStatesDiscreteActions
from app.discrete_states_discrete_actions import DiscreteStatesDiscreteActions

app = FastAPI()

env = Environment(loader=PackageLoader("app"), autoescape=select_autoescape())


@app.get("/")
async def main():
    template = env.get_template("templates/homepage.html")
    content = template.render()
    return HTMLResponse(content=content)


@app.get("/code/{item_id}")
async def render_code(item_id: str):
    template = env.get_template("code.html")
    filenames = {
        "1": "discrete_states_discrete_actions.py",
        "2": "continuous_states_discrete_actions.py",
        "3": "continuous_states_continuous_actions.py"
    }
    filename = filenames.get(item_id)
    if filename is None:
        return HTTPException(status_code=404, detail="Item not found")

    with open(f"app/{filename}", 'r', encoding='utf-8') as file:
        content = template.render(a_filename=filename, a_code=file.read())

    return HTMLResponse(content=content)


envs = {
    "1": DiscreteStatesDiscreteActions(),
    "2": ContinuousStatesDiscreteActions(),
    "3": ContinuousStatesContinuousActions()
}

for one_env in envs.keys():
    envs[one_env].action_space.seed(42)
    envs[one_env].reset(seed=42)
    envs[one_env].tick = 0


@app.get("/serve/{item_id}")
async def serve(item_id: str):
    excess_requests = JSONResponse(content=jsonable_encoder(
        {"result": "terminated due to excess number of requests - завершено по превышению количества запросов",
         "success": "false"}))
    if item_id in envs:
        example = envs[item_id]
        example.tick += 1
        if example.tick > 2000000:
            return excess_requests

        observation, reward, terminated, truncated, info = example.step(example.tick, example.action_space.sample())

    return JSONResponse(content=jsonable_encoder({"result": {"observation": observation,
                                                             "reward": reward,
                                                             "terminated": terminated,
                                                             "truncated": truncated,
                                                             "info": info}, "success": "true"}))
