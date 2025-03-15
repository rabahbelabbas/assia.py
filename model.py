import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

uploaded_file = st.file_uploader("📂 قم بتحميل ملف Excel", type=["xlsx", "xls" ,"csv"])
df = pd.DataFrame()
if uploaded_file:
    if uploaded_file.type == "text/csv":

        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

st.write("✅ تم تحميل البيانات بنجاح!")

        # تصنيفات الأشكال مع صورها
chart_categories = {
            "ثنائية الأبعاد": ["None" ,"Scatter", "Bar", "Line", "Area", "Heatmap", "Table", "Contour"],
            "التوزيعات": ["Pie", "Box", "Violin", "Histogram", "2D Histogram", "2D Contour Histogram"],
            "ثلاثية الأبعاد": ["3D Scatter", "3D Line", "3D Surface", "3D Mesh", "Cone", "Streamtube"],
            "متخصصة": ["Polar Scatter", "Polar Bar", "Ternary Scatter", "Sunburst", "Treemap", "Sankey"]
        }

cols = st.columns(2)
        # اختيار التصنيف
selected_category = cols[0].selectbox("اختر تصنيف المخطط:", list(chart_categories.keys()))

        # اختيار المخطط بناءً على الفئة المحددة
selected_chart = cols[1].selectbox("اختر نوع المخطط:", chart_categories[selected_category])
        # تأكيد المخطط المحدد
if selected_chart:
    st.subheader(f"🔹 المخطط المختار: {selected_chart}")

    # اختيار المتغيرات
    cols = st.columns(6)
    x_column = cols[0].selectbox("🛠 اختر المتغير X", df.columns)
    y_columns = cols[1].multiselect("⚙️ اختر متغير(ات) Y", df.columns)
    color_column = cols[2].selectbox("🎨 اختر المتغير اللوني (اختياري)", [None] + list(df.columns))
    size_column = cols[3].selectbox("📏 اختر متغير الحجم",
                                    [None] + list(df.columns)) if selected_chart == "Scatter" else None
    facet_row = cols[4].selectbox("📌 تقسيم الصفوف حسب", [None] + list(df.columns))
    facet_col = cols[5].selectbox("📌 تقسيم الأعمدة حسب", [None] + list(df.columns))

    # إنشاء المخطط
    fig = None
    if selected_chart == "Scatter":
        fig = px.scatter(df, x=x_column, y=y_columns, color=color_column, size=size_column, facet_row=facet_row,
                         facet_col=facet_col)
    elif selected_chart == "Bar":
        fig = px.bar(df, x=x_column, y=y_columns, color=color_column, facet_row=facet_row, facet_col=facet_col)
    elif selected_chart == "Line":
        fig = px.line(df, x=x_column, y=y_columns, color=color_column, facet_row=facet_row, facet_col=facet_col)
    elif selected_chart == "Histogram":
        fig = px.histogram(df, x=x_column, y=y_columns, color=color_column, facet_row=facet_row,
                           facet_col=facet_col)
    elif selected_chart == "Box":
        fig = px.box(df, x=x_column, y=y_columns, color=color_column, facet_row=facet_row, facet_col=facet_col)
    elif selected_chart == "Violin":
        fig = px.violin(df, x=x_column, y=y_columns, color=color_column, facet_row=facet_row,
                        facet_col=facet_col)
    elif selected_chart == "Pie":
        fig = px.pie(df, names=x_column, values=y_columns[0] if y_columns else None, color=color_column)
    elif selected_chart == "3D Scatter":
        fig = px.scatter_3d(df, x=x_column, y=y_columns[0] if y_columns else None, z=df.columns[2],
                            color=color_column)
    elif selected_chart == "Candlestick":
        fig = go.Figure(data=[
            go.Candlestick(x=df[x_column], open=df[y_columns[0]], high=df[y_columns[1]], low=df[y_columns[2]],
                           close=df[y_columns[3]])
        ])

    elif selected_chart == "OHLC":
        fig = go.Figure(data=[
            go.Ohlc(x=df[x_column], open=df[y_columns[0]], high=df[y_columns[1]], low=df[y_columns[2]],
                    close=df[y_columns[3]])
        ])

    elif selected_chart == "2D Histogram":
        fig = px.density_heatmap(df, x=x_column, y=y_columns[0], color_continuous_scale="Viridis")
    elif selected_chart == "2D Contour Histogram":
        fig = px.density_contour(df, x=x_column, y=y_columns[0], color=color_column)

    elif selected_chart == "3D Line":
        fig = go.Figure(
            data=[go.Scatter3d(x=df[x_column], y=df[y_columns[0]], z=df[df.columns[2]], mode="lines",
                               marker=dict(size=5))])
    elif selected_chart == "3D Surface":
        fig = go.Figure(data=[go.Surface(z=df.values)])
    elif selected_chart == "3D Mesh":
        fig = go.Figure(
            data=[go.Mesh3d(x=df[x_column], y=df[y_columns[0]], z=df[df.columns[2]], color=color_column)])
    elif selected_chart == "Cone":
        fig = go.Figure(data=[
            go.Cone(x=df[x_column], y=df[y_columns[0]], z=df[df.columns[2]], u=df[x_column], v=df[y_columns[0]],
                    w=df[df.columns[2]])])

    elif selected_chart == "Polar Scatter":
        fig = px.scatter_polar(df, r=x_column, theta=y_columns[0], color=color_column)
    elif selected_chart == "Polar Bar":
        fig = px.bar_polar(df, r=x_column, theta=y_columns[0], color=color_column)
    elif selected_chart == "Ternary Scatter":
        fig = px.scatter_ternary(df, a=x_column, b=y_columns[0], c=df[df.columns[2]], color=color_column)
    elif selected_chart == "Sunburst":
        fig = px.sunburst(df, path=[x_column, y_columns[0]], values=df[df.columns[2]], color=color_column)
    elif selected_chart == "Treemap":
        fig = px.treemap(df, path=[x_column, y_columns[0]], values=df[df.columns[2]], color=color_column)
    elif selected_chart == "Sankey":
        fig = go.Figure(go.Sankey(
            node=dict(label=df[x_column]),
            link=dict(source=df[y_columns[0]], target=df[y_columns[1]], value=df[y_columns[2]])
        ))
    else :
        st.write("اختر شكل معين")

    if fig:
        st.plotly_chart(fig, use_container_width=True)
