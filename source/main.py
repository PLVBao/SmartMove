import streamlit as st
from db import fetch_df, execute, get_count


# Page settings
st.set_page_config(
    page_title="SmartMovers Management",
    page_icon="🚚",
    layout="wide"
)


# Custom UI style
st.markdown("""
<style>
.block-container {
    padding-top: 2rem;
    max-width: 1400px;
}

.main-title {
    font-size: 42px;
    font-weight: 800;
    margin-bottom: 4px;
}

.sub-title {
    color: #6b7280;
    margin-bottom: 28px;
    font-size: 16px;
}

.card {
    padding: 22px;
    border-radius: 14px;
    background-color: #ffffff;
    box-shadow: 0 2px 12px rgba(0,0,0,0.08);
    border: 1px solid #eeeeee;
}

.metric-label {
    color: #6b7280;
    font-size: 15px;
    font-weight: 500;
}

.metric-value {
    font-size: 34px;
    font-weight: 800;
}
</style>
""", unsafe_allow_html=True)


# Header
st.markdown(
    '<div class="main-title">🚚 SmartMovers Management System</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="sub-title">Operational dashboard for transport jobs, loads, customers and cost reports.</div>',
    unsafe_allow_html=True
)


# Sidebar navigation
menu = st.sidebar.radio(
    "Menu",
    ["Dashboard", "Data Entry", "Reports", "Database Tables"]
)


# =========================
# DASHBOARD
# =========================

if menu == "Dashboard":
    st.header("Dashboard")

    try:
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.markdown(f"""
            <div class="card">
                <div class="metric-label">Customers</div>
                <div class="metric-value">{get_count("Customer")}</div>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
            <div class="card">
                <div class="metric-label">Depots</div>
                <div class="metric-value">{get_count("Depot")}</div>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            st.markdown(f"""
            <div class="card">
                <div class="metric-label">Products</div>
                <div class="metric-value">{get_count("Product")}</div>
            </div>
            """, unsafe_allow_html=True)

        with col4:
            st.markdown(f"""
            <div class="card">
                <div class="metric-label">Jobs</div>
                <div class="metric-value">{get_count("Job")}</div>
            </div>
            """, unsafe_allow_html=True)

        st.write("")

        col5, col6, col7 = st.columns(3)

        with col5:
            st.markdown(f"""
            <div class="card">
                <div class="metric-label">Loads</div>
                <div class="metric-value">{get_count("Load")}</div>
            </div>
            """, unsafe_allow_html=True)

        with col6:
            st.markdown(f"""
            <div class="card">
                <div class="metric-label">Transport Units</div>
                <div class="metric-value">{get_count("TransportUnit")}</div>
            </div>
            """, unsafe_allow_html=True)

        with col7:
            st.markdown(f"""
            <div class="card">
                <div class="metric-label">Containers</div>
                <div class="metric-value">{get_count("Container")}</div>
            </div>
            """, unsafe_allow_html=True)

        st.divider()

        st.subheader("Job Cost Overview")

        df = fetch_df("""
            SELECT job_id, customer_id, customer_name, total_cost
            FROM JobCost
            ORDER BY job_id
        """)

        st.dataframe(df, use_container_width=True, hide_index=True)

    except Exception as e:
        st.error(f"Database error: {e}")


# =========================
# DATA ENTRY
# =========================

elif menu == "Data Entry":
    st.header("Data Entry")

    tab1, tab2, tab3, tab4 = st.tabs([
        "Customer",
        "Product",
        "Job",
        "Load"
    ])


    # ---------- Customer ----------
    with tab1:
        st.subheader("Customer Registration")

        with st.form("add_customer_form"):
            customer_id = st.text_input("Customer ID", placeholder="C010")
            name = st.text_input("Customer Name", placeholder="Example Chemical Co.")
            address = st.text_input("Address", placeholder="Example address")
            phone = st.text_input("Phone Number", placeholder="0999999999")
            category = st.selectbox("Customer Category", ["Category 1", "Category 2", "Category 3"])

            submitted = st.form_submit_button("Save Customer")

            if submitted:
                try:
                    if not customer_id.strip() or not name.strip():
                        st.warning("Customer ID and Customer Name are required.")
                    else:
                        execute("""
                            INSERT INTO Customer (customer_id, name, address, phone, category)
                            VALUES (%s, %s, %s, %s, %s)
                        """, (
                            customer_id.strip(),
                            name.strip(),
                            address.strip(),
                            phone.strip(),
                            category
                        ))

                        st.success("Customer saved successfully.")
                        st.rerun()

                except Exception as e:
                    st.error(f"Unable to save customer: {e}")

        st.subheader("Customer List")
        st.dataframe(
            fetch_df("SELECT * FROM Customer ORDER BY customer_id"),
            use_container_width=True,
            hide_index=True
        )


    # ---------- Product ----------
    with tab2:
        st.subheader("Product Registration")

        with st.form("add_product_form"):
            product_id = st.text_input("Product ID", placeholder="P010")
            product_name = st.text_input("Product Name", placeholder="Chemical product")
            risk_type = st.selectbox("Risk Type", ["No Risk", "High Risk"])

            submitted = st.form_submit_button("Save Product")

            if submitted:
                try:
                    if not product_id.strip() or not product_name.strip():
                        st.warning("Product ID and Product Name are required.")
                    else:
                        execute("""
                            INSERT INTO Product (product_id, product_name, risk_type)
                            VALUES (%s, %s, %s)
                        """, (
                            product_id.strip(),
                            product_name.strip(),
                            risk_type
                        ))

                        st.success("Product saved successfully.")
                        st.rerun()

                except Exception as e:
                    st.error(f"Unable to save product: {e}")

        st.subheader("Product List")
        st.dataframe(
            fetch_df("SELECT * FROM Product ORDER BY product_id"),
            use_container_width=True,
            hide_index=True
        )


    # ---------- Job ----------
    with tab3:
        st.subheader("Job Registration")

        customers = fetch_df("""
            SELECT customer_id, name
            FROM Customer
            ORDER BY customer_id
        """)

        depots = fetch_df("""
            SELECT depot_id, location
            FROM Depot
            ORDER BY depot_id
        """)

        customer_options = {
            f"{row['customer_id']} - {row['name']}": row["customer_id"]
            for _, row in customers.iterrows()
        }

        depot_options = {
            f"{row['depot_id']} - {row['location']}": row["depot_id"]
            for _, row in depots.iterrows()
        }

        with st.form("add_job_form"):
            job_id = st.text_input("Job ID", placeholder="J010")

            customer_label = st.selectbox(
                "Customer",
                list(customer_options.keys())
            )

            depot_label = st.selectbox(
                "Depot",
                list(depot_options.keys())
            )

            start_location = st.text_input("Start Location", placeholder="Ho Chi Minh City")
            destination = st.text_input("Destination", placeholder="Dong Nai")

            submitted = st.form_submit_button("Save Job")

            if submitted:
                try:
                    if not job_id.strip() or not start_location.strip() or not destination.strip():
                        st.warning("Job ID, Start Location and Destination are required.")
                    else:
                        execute("""
                            INSERT INTO Job (job_id, customer_id, depot_id, start_location, destination)
                            VALUES (%s, %s, %s, %s, %s)
                        """, (
                            job_id.strip(),
                            customer_options[customer_label],
                            depot_options[depot_label],
                            start_location.strip(),
                            destination.strip()
                        ))

                        st.success("Job saved successfully.")
                        st.rerun()

                except Exception as e:
                    st.error(f"Unable to save job: {e}")

        st.subheader("Job List")
        st.dataframe(
            fetch_df("""
                SELECT 
                    j.job_id,
                    c.name AS customer_name,
                    d.location AS depot_location,
                    j.start_location,
                    j.destination
                FROM Job j
                JOIN Customer c ON j.customer_id = c.customer_id
                JOIN Depot d ON j.depot_id = d.depot_id
                ORDER BY j.job_id
            """),
            use_container_width=True,
            hide_index=True
        )


    # ---------- Load ----------
    with tab4:
        st.subheader("Load Registration")

        jobs = fetch_df("""
            SELECT job_id
            FROM Job
            ORDER BY job_id
        """)

        products = fetch_df("""
            SELECT product_id, product_name
            FROM Product
            ORDER BY product_id
        """)

        units = fetch_df("""
            SELECT transport_unit_id, lorry
            FROM TransportUnit
            ORDER BY transport_unit_id
        """)

        job_options = [row["job_id"] for _, row in jobs.iterrows()]

        product_options = {
            f"{row['product_id']} - {row['product_name']}": row["product_id"]
            for _, row in products.iterrows()
        }

        unit_options = {
            f"{row['transport_unit_id']} - {row['lorry']}": row["transport_unit_id"]
            for _, row in units.iterrows()
        }

        with st.form("add_load_form"):
            load_id = st.text_input("Load ID", placeholder="L010")

            job_id = st.selectbox(
                "Job",
                job_options
            )

            product_label = st.selectbox(
                "Product",
                list(product_options.keys())
            )

            unit_label = st.selectbox(
                "Transport Unit",
                list(unit_options.keys())
            )

            load_size = st.selectbox("Load Size", ["small", "medium", "large"])

            submitted = st.form_submit_button("Save Load")

            if submitted:
                try:
                    if not load_id.strip():
                        st.warning("Load ID is required.")
                    else:
                        execute("""
                            INSERT INTO `Load` (load_id, job_id, product_id, transport_unit_id, load_size)
                            VALUES (%s, %s, %s, %s, %s)
                        """, (
                            load_id.strip(),
                            job_id,
                            product_options[product_label],
                            unit_options[unit_label],
                            load_size
                        ))

                        st.success("Load saved successfully.")
                        st.rerun()

                except Exception as e:
                    st.error(f"Unable to save load: {e}")

        st.subheader("Load List")
        st.dataframe(
            fetch_df("""
                SELECT 
                    l.load_id,
                    l.job_id,
                    p.product_name,
                    p.risk_type,
                    l.transport_unit_id,
                    l.load_size
                FROM `Load` l
                JOIN Product p ON l.product_id = p.product_id
                ORDER BY l.load_id
            """),
            use_container_width=True,
            hide_index=True
        )


# =========================
# REPORTS
# =========================

elif menu == "Reports":
    st.header("Reports")

    report_type = st.selectbox(
        "Report Type",
        [
            "Job Cost Summary",
            "Load Pricing Details",
            "Job Assignment Overview",
            "Transport Unit Allocation",
            "Depot Workload Summary",
            "Customer Load Summary"
        ]
    )

    if report_type == "Job Cost Summary":
        st.subheader("Job Cost Summary")
        st.caption("Total transport cost calculated for each job.")

        df = fetch_df("""
            SELECT job_id, customer_id, customer_name, total_cost
            FROM JobCost
            ORDER BY job_id
        """)

        st.dataframe(df, use_container_width=True, hide_index=True)

    elif report_type == "Load Pricing Details":
        st.subheader("Load Pricing Details")
        st.caption("Pricing based on customer category, product risk type and load size.")

        df = fetch_df("""
            SELECT 
                l.load_id,
                j.job_id,
                c.name AS customer_name,
                c.category AS customer_category,
                p.product_name,
                p.risk_type,
                l.load_size,
                pr.price
            FROM `Load` l
            JOIN Job j ON l.job_id = j.job_id
            JOIN Customer c ON j.customer_id = c.customer_id
            JOIN Product p ON l.product_id = p.product_id
            JOIN PaymentRule pr 
                ON pr.customer_category = c.category
               AND pr.product_risk = p.risk_type
               AND pr.load_size = l.load_size
            ORDER BY j.job_id, l.load_id
        """)

        st.dataframe(df, use_container_width=True, hide_index=True)

    elif report_type == "Job Assignment Overview":
        st.subheader("Job Assignment Overview")
        st.caption("Customer and depot information for each job.")

        df = fetch_df("""
            SELECT 
                j.job_id,
                c.name AS customer_name,
                c.category,
                d.location AS depot_location,
                j.start_location,
                j.destination
            FROM Job j
            JOIN Customer c ON j.customer_id = c.customer_id
            JOIN Depot d ON j.depot_id = d.depot_id
            ORDER BY j.job_id
        """)

        st.dataframe(df, use_container_width=True, hide_index=True)

    elif report_type == "Transport Unit Allocation":
        st.subheader("Transport Unit Allocation")
        st.caption("Assigned containers for transport units.")

        df = fetch_df("""
            SELECT 
                tu.transport_unit_id,
                tu.lorry,
                tu.driver,
                tu.assistant,
                c.container_id,
                c.container_type
            FROM TransportUnit tu
            JOIN Transport t ON tu.transport_unit_id = t.transport_unit_id
            JOIN Container c ON t.container_id = c.container_id
            ORDER BY tu.transport_unit_id
        """)

        st.dataframe(df, use_container_width=True, hide_index=True)

    elif report_type == "Depot Workload Summary":
        st.subheader("Depot Workload Summary")
        st.caption("Number of jobs assigned to each depot.")

        df = fetch_df("""
            SELECT 
                d.depot_id,
                d.location,
                COUNT(j.job_id) AS total_jobs
            FROM Depot d
            LEFT JOIN Job j ON d.depot_id = j.depot_id
            GROUP BY d.depot_id, d.location
            ORDER BY d.depot_id
        """)

        st.dataframe(df, use_container_width=True, hide_index=True)

    elif report_type == "Customer Load Summary":
        st.subheader("Customer Load Summary")
        st.caption("Number of loads associated with each customer.")

        df = fetch_df("""
            SELECT 
                c.customer_id,
                c.name AS customer_name,
                COUNT(l.load_id) AS total_loads
            FROM Customer c
            JOIN Job j ON c.customer_id = j.customer_id
            JOIN `Load` l ON j.job_id = l.job_id
            GROUP BY c.customer_id, c.name
            ORDER BY c.customer_id
        """)

        st.dataframe(df, use_container_width=True, hide_index=True)


# =========================
# DATABASE TABLES
# =========================

elif menu == "Database Tables":
    st.header("Database Tables")

    table = st.selectbox(
        "Table",
        [
            "Customer",
            "Depot",
            "Product",
            "Container",
            "TransportUnit",
            "Transport",
            "Job",
            "Load",
            "PaymentRule",
            "JobCost"
        ]
    )

    search = st.text_input("Search", placeholder="Search by ID, name, location...")

    if table == "Load":
        df = fetch_df("SELECT * FROM `Load`")
    elif table == "JobCost":
        df = fetch_df("SELECT * FROM JobCost")
    else:
        df = fetch_df(f"SELECT * FROM `{table}`")

    if search.strip():
        search_lower = search.lower()
        df = df[
            df.astype(str)
            .apply(lambda row: row.str.lower().str.contains(search_lower).any(), axis=1)
        ]

    st.dataframe(df, use_container_width=True, hide_index=True)