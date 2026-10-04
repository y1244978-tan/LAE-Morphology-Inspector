from database import get_lae_by_ew

df = get_lae_by_ew(50)

print(df[["id", "ew"]].head(20))
print("件数:", len(df))