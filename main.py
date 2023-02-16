import pandas as pd
import plotly.express as px

"""Show numeric output in decimal format e.g., 2.15"""
pd.options.display.float_format = "{:,.2f}".format

df_apps = pd.read_csv('apps.csv')
# print(df_apps.shape)
# print(df_apps.head())
# print(df_apps.sample(10))

"""Remove the columns called Last_Updated and Android_Version from the DataFrame. We will not use these columns."""
df_apps.drop(labels=["Last_Updated", "Android_Ver"], axis=1, inplace=True)
# print(df_apps.head())

"""How may rows have a NaN value (not-a-number) in the Ratings column? Create DataFrame called df_apps_clean that does not include these rows."""
# nan_rows = df_apps[df_apps.isna().any(axis=1)]
nan_rows = df_apps[df_apps["Rating"].isna()]
# print(nan_rows.shape)
# print(nan_rows.head())

df_apps_clean = df_apps.dropna()
# print(df_apps_clean.shape)
# print(df_apps_clean.head())

"""Are there any duplicates in data? Check for duplicates using the .duplicated() function. How many entries can you find for the "Instagram" app?"""
duplicated_rows = df_apps_clean[df_apps_clean.duplicated()]
# print(duplicated_rows.shape)
# print(duplicated_rows.head())

# print(df_apps_clean.shape)
dup_example = df_apps_clean[df_apps_clean["App"] == "Instagram"]
# print(dup_example)

df_apps_clean = df_apps_clean.drop_duplicates(subset=["App", "Type", "Price"])
# print(df_apps_clean.shape)

"""Identify which apps are the highest rated."""
sort_rating = df_apps_clean.sort_values("Rating", ascending=False).head()
# print(highest_rating)

"""What's the size in megabytes (MB) of the largest Android apps in the Google Play Store."""
sort_size = df_apps_clean.sort_values("Size_MBs", ascending=False).head()
# print(sort_size)

"""Which apps have the highest number of reviews?"""
sort_reviews = df_apps_clean.sort_values("Reviews", ascending=False).head(10)
# print(sort_reviews)

"""Plotly Pie and Donut Charts - Visualise Categorical Data: Content Ratings"""
ratings = df_apps_clean["Content_Rating"].value_counts()
# print(type(ratings))
# print(ratings)

# fig1 = px.pie(labels=ratings.index, values=ratings.values)
# fig1.show()

# fig2 = px.pie(labels=ratings.index, values=ratings.values, title="Content Rating", names=ratings.index)
# fig2.update_traces(textposition="outside", textinfo="percent+label")
# fig2.show()

# fig3 = px.pie(labels=ratings.index, values=ratings.values, title="Content Rating", names=ratings.index, hole=0.6)
# fig3.update_traces(textposition='inside', textfont_size=15, textinfo='percent')
# fig3.show()

"""Numeric Type Conversion: Examine the Number of Installs"""
describe = df_apps_clean["Installs"].describe()
# print(describe)

# df_apps_clean.info()

"""How many apps had over 1 billion (that's right - BILLION) installations? How many apps just had a single install?"""
app_installs_before = df_apps_clean[["Installs", "App"]].groupby("Installs").count()
# print(app_installs)

"""Convert the number of installations (the Installs column) to a numeric data type."""
# df_apps_clean["Installs"] = df_apps_clean["Installs"].astype(str).str.replace(",", "").astype(int)
df_apps_clean["Installs"] = df_apps_clean["Installs"].astype(str).str.replace(",", "")
df_apps_clean["Installs"] = pd.to_numeric(df_apps_clean["Installs"])
app_installs_after = df_apps_clean[["Installs", "App"]].groupby("Installs").count()
# print(app_installs_after)

"""datatype conversion example"""
dic = {
    "a": ["5,000", "1,000", "3,000"],
    "b": ["1,000", "3,000", "5,000"],
    "c": ["3,000", "1,000", "5,000"],
}

df = pd.DataFrame(data=dic)
# print(df)
# print(df["a"])

df["a"] = df["a"].astype(str).str.replace(",", "").astype("int")
# print(df["a"])
# print(df["a"].dtypes)

val = df.loc[:, "a"]
# print(val)

"""Convert the price column to numeric data. Then investigate the top 20 most expensive apps in the dataset."""
df_apps_clean["Price"] = df_apps_clean["Price"].astype(str).str.replace("$", "", regex=False).astype(float)
# print(df_apps_clean.dtypes)
sort_price = df_apps_clean.sort_values("Price", ascending=False)[:20]
# print(sort_price)

"""The most expensive apps sub $250"""
df_apps_clean = df_apps_clean[df_apps_clean["Price"] < 250]
top20_price = df_apps_clean.sort_values("Price", ascending=False)
# print(top20_price)

"""Highest Grossing Paid Apps. Add Revenue column"""
df_apps_clean["Revenue_Estimate"] = df_apps_clean["Installs"].mul(df_apps_clean["Price"])
sort_revenue = df_apps_clean.sort_values("Revenue_Estimate", ascending=False)[:10]
# print(sort_revenue)

"""Plotly Bar Charts & Scatter Plots: Analysing App Categories"""
# find the number of different categories:
unique_category_count = df_apps_clean["Category"].nunique()
# print(unique_category_count)
unique_category = df_apps_clean["Category"].unique()
# print(unique_category)

# Calculate the number of apps per category
top10_category = df_apps_clean["Category"].value_counts()[:10]
# print(top10_category)

# bar = px.bar(x=top10_category.index, y=top10_category.values)
# bar.show()

"""Horizontal Bar Chart - Most Popular Categories (Highest Downloads)"""
category_installs = df_apps_clean.groupby("Category").agg({"Installs": pd.Series.sum})
category_installs.sort_values("Installs", ascending=True, inplace=True)
# print(category_installs[:5])

# h_bar = px.bar(x=category_installs["Installs"], y=category_installs.index, orientation="h", title="Category Popularity")
# h_bar.update_layout(xaxis_title="Number of Downloads", yaxis_title="Category")
# h_bar.show()

"""Category Concentration - Downloads vs. Competition"""
# create a DataFrame that has the number of apps in one column and the number of installs in another:
df_app_installs = df_apps_clean.groupby("Category").agg({"App": pd.Series.count, "Installs": pd.Series.sum})
# print(f"The dimensions of the DataFrame are: {df_app_installs.shape}")
app_installs = df_app_installs.sort_values("Installs", ascending=False)
# print(app_installs)

cat_number = df_apps_clean.groupby("Category").agg({"App": pd.Series.count})
cat_merged_df = pd.merge(cat_number, category_installs, on="Category", how="inner")
# print(f"The dimensions of the DataFrame are: {cat_merged_df.shape}")
sorted_merged_df = cat_merged_df.sort_values("Installs", ascending=False)
# print(sorted_merged_df)

# scatter = px.scatter(cat_merged_df,
#                      x="App",
#                      y="Installs",
#                      title="Category Concentration",
#                      size="App",
#                      hover_name=cat_merged_df.index,
#                      color="Installs")
#
# scatter.update_layout(xaxis_title="Number of Apps (Lower=More Concentrated)",
#                       yaxis_title="Installs",
#                       yaxis=dict(type="log"))
#
# scatter.show()

"""Extracting Nested Data from a Column"""
# print(len(df_apps_clean["Genres"].unique()))
sort_genre = df_apps_clean["Genres"].value_counts().sort_values()[:5]
# print(sort_genre)

stack = df_apps_clean["Genres"].astype(str).str.split(";", expand=True).stack()
# print(f"We now have a single column with shape: {stack.shape}")
# print(type(stack))
# print(stack)

num_genres = stack.value_counts()
# print(f"Number of genres: {len(num_genres)}")
# print(num_genres)

"""Colour Scales in Plotly Charts - Competition in Genres"""
# Can you create this chart with the Series containing the genre data?
# bar = px.bar(x=num_genres.index[:15],
#              y=num_genres.values[:15],
#              title="Top Genres",
#              hover_name=num_genres.index[:15],
#              color=num_genres.values[:15],
#              color_continuous_scale="Agsunset")
#
# bar.update_layout(xaxis_title="Genre",
#                   yaxis_title="Number of Apps",
#                   coloraxis_showscale=False)
#
# bar.show()

"""Grouped Bar Charts: Free vs. Paid Apps per Category"""
app_types = df_apps_clean["Type"].value_counts()
# print(app_types)

df_free_vs_paid = df_apps_clean.groupby(["Category", "Type"], as_index=False).agg({"App": pd.Series.count})
# print(df_free_vs_paid)
sort_type = df_free_vs_paid.sort_values("App")
# print(sort_type)

"""Use the plotly express bar chart examples and the .bar() API reference to create this bar chart:"""
# g_bar = px.bar(df_free_vs_paid,
#                x="Category",
#                y="App",
#                title="Free vs Paid Apps by Category",
#                color="Type",
#                barmode="group")
#
# g_bar.update_layout(xaxis_title="Category",
#                     yaxis_title="Number of Apps",
#                     xaxis={"categoryorder": "total descending"},
#                     yaxis=dict(type="log"))
#
# g_bar.show()

"""Plotly Box Plots: Lost Downloads for Paid Apps"""
# Create a box plot that shows the number of Installs for free versus paid apps.
# box = px.box(df_apps_clean,
#              x="Type",
#              y="Installs",
#              color="Type",
#              notched=True,
#              points="all",
#              title="How Many Downloads are Paid Apps Giving Up?")
#
# box.update_layout(yaxis=dict(type="log"))
#
# box.show()

"""Plotly Box Plots: Revenue by App Category"""
# print(df_apps_clean.head())
df_paid_apps = df_apps_clean[df_apps_clean["Type"] == "Paid"]

# box = px.box(df_paid_apps,
#              x="Category",
#              y="Revenue_Estimate",
#              title="How Much Can Paid Apps Earn?")
#
# box.update_layout(xaxis_title="Category",
#                   yaxis_title="Paid App Ballpark Revenue",
#                   xaxis={"categoryorder": "min ascending"},
#                   yaxis=dict(type="log"))
#
# box.show()

"""How Much Can You Charge? Examine Paid App Pricing Strategies by Category"""
median_price = df_paid_apps["Price"].median()
# print(median_price)

# box = px.box(df_paid_apps,
#              x="Category",
#              y="Price",
#              title="Price per Category")
#
# box.update_layout(xaxis_title="Category",
#                   yaxis_title="Paid App Price",
#                   xaxis={"categoryorder": "max descending"},
#                   yaxis=dict(type="log"))
#
# box.show()

