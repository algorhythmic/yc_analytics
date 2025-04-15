# Overview
Project Name: YC Analytics Dashboard

Purpose: To provide data-driven insights into Y Combinator companies by ingesting CSV exports of the public API, processing and transforming the data, and rendering interactive charts and views on a responsive dashboard.

End Users: Data analysts, internal teams, and external stakeholders interested in trends among YC companies.

Hosting Platform: Streamlit Community Cloud for simple and rapid deployment.

## Goals and Objectives
Rapid Prototyping: Leverage Python’s streamlined libraries for fast development and iteration.

Interactive Visualization: Build an intuitive dashboard using Plotly with responsive charts and filtering options.

Maintainability: Use caching and minimal configuration to reduce overhead and ensure ease of updates.

Scalable Simplicity: Enable easy expansion if additional data sources or backend features are needed.

## Pipeline Overview
Data Ingestion:

Fetch CSV files (generated from the JSON endpoints in the yc-oss API) using an automated process.

Use Python (Pandas) for parsing and cleaning the CSV data.

Data Transformation & Storage:

(Optional) Transform and normalize data into a relational schema (potentially in SQLite) if persistent or historical analysis is required.

Alternatively, leverage in-memory Pandas DataFrames for real-time analysis since the dataset is relatively small.

Visualization and Dashboard:

Use Plotly for charting within Streamlit to render interactive visualizations.

Organize the dashboard layout with a sidebar for filters and a main panel for dynamic charts.

Deployment:

Deploy on Streamlit Community Cloud using GitHub integration for a one-click and auto-updating deployment setup.

## Data Ingestion
Source: CSV files derived from the Y Combinator companies API (referencing the GitHub repository).

Method:

Use Python scripts to download and update CSV exports on a schedule (daily updates are available).

Utilize Pandas’ read_csv() function to load and preprocess the CSV files.

Caching:

Implement caching using Streamlit’s @st.cache_data decorator to store function outputs for a specified duration, reducing redundant file reads and improving performance.

## Data Schema and (Optional) Database Design
For simple analytics, storing the data in memory via Pandas is acceptable. However, if persistence or historical trend analysis is desired, design a lightweight relational schema using duckDB.

https://yc-oss.github.io/api/companies/all.json APIData Schema:
Property	Type	Description
id	number	The company's ID decided by Y Combinator
name	string	The company's name
slug	string	The company's human-readable slug
former_names	string[]	The company's former names, if the company was renamed
small_logo_thumb_url	string	The URL of the company's logo as a square hosted by Y Combinator
website	string	The company's website URL
all_locations	string	The company's locations separated by colons (;)
long_description	string	The company's long description
one_liner	string	The company's one-liner description
team_size	number	The company's team size
highlight_black	boolean	Whether the company is highlighted for Black founders
highlight_latinx	boolean	Whether the company is highlighted for Hispanic/Latino founders
highlight_women	boolean	Whether the company is highlighted for women founders
industry	string	The company's industry
subindustry	string	The company's subindustry
launched_at	number	The company's launch date as a Unix timestamp
tags	string[]	The company's tags
top_company	boolean	Whether the company is a top company
isHiring	boolean	Whether the company is hiring
nonprofit	boolean	Whether the company is a nonprofit
batch	string	The company's batch
status	string	The company's status
industries	string[]	The company's industries
regions	string[]	The company's regions
stage	string	The company's stage
app_video_public	boolean	Whether the company's app video is public
demo_day_video_public	boolean	Whether the company's demo day video is public
app_answers	object	The company's app answers
question_answers	boolean	Whether the company's question answers are public
url	string	The company's URL on the Y Combinator website
api	string	The company's API endpoint from this repository

## Data Transformation and Processing 
### Preprocessing Steps:

Clean missing or malformed data

Convert list/JSON fields into string representations or Python lists

Format timestamps into human-readable dates

### Tools:

Pandas for data manipulation

Python’s built-in JSON library for handling nested structures

### Caching:

Use cached functions in Streamlit to minimize reprocessing on every run.

## Charting and Layout Recommendations
Using Streamlit’s integration with Plotly, the dashboard should be intuitive and segmented into clearly defined sections.

### Recommended Chart Types
Line Chart:

Display trends over time such as the number of companies launched per month or growth in team size.

Bar Chart:

Compare metrics such as the distribution of companies by industry, batch, or tag.

Pie Chart:

Visualize market share or percentage breakdowns, such as hiring status or company status.

Scatter Chart:

Explore relationships between features such as team size versus launch date.

Interactive Filters:

Sidebar selectors (using st.selectbox and st.multiselect) for filtering by industry, batch, or region.

### Dashboard Layout
Header:

Title (e.g., “YC Companies Analytics Dashboard”) and summary metrics (total companies, top companies, etc.).

Sidebar:

Filter options including date ranges, industries, batches, and hiring status.

Navigation links if there are multiple dashboard views.

Main Panel:

Top Row: Overview charts; a bar chart for industry distribution and a pie chart for batch distribution.

Middle Section: Time series visualizations using line charts for trends over time.

Bottom Section: Detailed listings or data tables allowing users to drill down into specific company details.

Responsive Design:

Use Streamlit’s layout features such as st.columns to ensure charts reflow appropriately on different screen sizes.

Maintain consistent color schemes and labeling for clarity.

Streamlit’s built-in charting support complements Plotly’s advanced interactive features, ensuring high user engagement.

## Hosting and Deployment on Streamlit Community Cloud
Repository Integration:

Code should be maintained in a GitHub repository.

Follow the deployment steps on the Streamlit Community Cloud by linking the repository and selecting your main Python file.

Deployment Steps:

Ensure requirements.txt includes dependencies such as Streamlit, Pandas, Plotly, and any other third-party libraries.

Configure environment variables and secrets if needed using a secrets.toml file.

Upon pushing changes via Git, the app will auto-deploy on Community Cloud, leveraging real-time logs to monitor resource usage and performance.

Resource Considerations:

Be mindful of Community Cloud limits (e.g., RAM limitations).

Optimize data processing and caching to reduce memory footprint.

## Non-Functional Requirements
Performance:

Minimize initial load times through effective caching and lazy-loading of charts.

Usability:

Ensure the interface is intuitive through consistent layout, tool-tips, and clear labels.

Flexibility:

Design the architecture to allow external API data to be replaced or updated without a complete overhaul.

Maintainability:

Write well-documented, modular code to facilitate maintenance and future expansion.