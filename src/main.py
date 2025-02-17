from solver.matrix_solver import solve
from fastapi import FastAPI, Body, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI(
    title="Cyberpunk Solver",
    openapi_url="/openapi.json",
    openapi_tags=["solver"],
    docs_url="/docs",
    redoc_url="/redoc",
)


class SolveRequest(BaseModel):
    matrix: List[List[str]]
    buffer_size: int
    sequences: List[List[str]]


@app.post("/solve", tags=["solver"])
async def solve_sudoku(request: SolveRequest = Body(...)):
    if len(request.matrix) != 7 or any(len(row) != 7 for row in request.matrix):
        raise HTTPException(400, "The matrix must be a 7x7 array")
    return solve(request.matrix, request.sequences, request.buffer_size)
