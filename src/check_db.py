from database import get_ranked_galaxies

df = get_ranked_galaxies(
    sample="LAE",
    metric="asymmetry",
    order="DESC",
    limit_num=10
)

print(df[[
    "id",
    "asymmetry"
]])
