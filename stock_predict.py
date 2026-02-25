
import numpy as np
import pandas as pd
import yfinance as yf
import streamlit as st
import ta
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor

st.title("📊 Stock Price Forecasting System")
st.markdown("Comparative Analysis of Machine Learning Models for Time-Series Prediction")

# ---------------- SIDEBAR ----------------
st.sidebar.header("Project Info")
st.sidebar.write("Author: Tanisha Patil")
st.sidebar.write("Domain: Time Series Forecasting")
st.sidebar.write("Models Used: Linear Regression, Random Forest")

# ---------------- STOCK SELECTION ----------------
stock = st.selectbox(
    "Select Stock",
    ["TCS.NS", "RELIANCE.NS", "INFY.NS", "AAPL", "^NSEI"]
)

# ---------------- DATA DOWNLOAD ----------------
data = yf.download(stock, start="2018-01-01")

if data.empty:
    st.error("Data not loaded")
    st.stop()

st.subheader("Raw Data Preview")
st.dataframe(data.tail())

# Fix Close
close = data["Close"]
if isinstance(close, pd.DataFrame):
    close = close.iloc[:, 0]

# ---------------- INDICATORS ----------------
data["MA"] = ta.trend.sma_indicator(close, window=14)
data["RSI"] = ta.momentum.rsi(close, window=14)

# 🔥 Volatility Added
data["Volatility"] = data["Close"].rolling(window=14).std()

# Returns + Cumulative Returns
data["Returns"] = data["Close"].pct_change()
data["Cumulative Returns"] = (1 + data["Returns"]).cumprod()

data = data.dropna()

features = data[["Close", "MA", "RSI", "Volatility"]]

# ---------------- HEATMAP ----------------
st.subheader("Feature Correlation Heatmap")
fig_heat, ax_heat = plt.subplots()
sns.heatmap(features.corr(), annot=True, cmap="coolwarm", ax=ax_heat)
st.pyplot(fig_heat)

# ---------------- SCALING ----------------
scaler = MinMaxScaler()
scaled = scaler.fit_transform(features)

# ---------------- ROLLING WINDOW ----------------
X, y = [], []
for i in range(30, len(scaled)):
    X.append(scaled[i-30:i])
    y.append(scaled[i][0])

X, y = np.array(X), np.array(y)

split = int(0.8 * len(X))
X_train, X_test = X[:split], X[split:]
y_train, y_test = y[:split], y[split:]

# ---------------- MODELS ----------------
lr_model = LinearRegression()
lr_model.fit(X_train.reshape(X_train.shape[0], -1), y_train)
lr_pred = lr_model.predict(X_test.reshape(X_test.shape[0], -1))

rf_model = RandomForestRegressor()
rf_model.fit(X_train.reshape(X_train.shape[0], -1), y_train)
rf_pred = rf_model.predict(X_test.reshape(X_test.shape[0], -1))

# ---------------- INVERSE SCALING ----------------
def inverse_close(pred_array):
    temp = np.zeros((len(pred_array), features.shape[1]))
    temp[:, 0] = pred_array
    return scaler.inverse_transform(temp)[:, 0]

y_test_actual = inverse_close(y_test)
lr_pred_actual = inverse_close(lr_pred)
rf_pred_actual = inverse_close(rf_pred)

# ---------------- METRICS ----------------
lr_rmse = np.sqrt(mean_squared_error(y_test_actual, lr_pred_actual))
rf_rmse = np.sqrt(mean_squared_error(y_test_actual, rf_pred_actual))
lr_r2 = r2_score(y_test_actual, lr_pred_actual)

direction_acc = np.mean(
    np.sign(lr_pred_actual[1:] - lr_pred_actual[:-1]) ==
    np.sign(y_test_actual[1:] - y_test_actual[:-1])
)

# ---------------- MODEL COMPARISON ----------------
st.subheader("Model Comparison")
results = pd.DataFrame({
    "Model": ["Linear Regression", "Random Forest"],
    "RMSE (Real Price)": [lr_rmse, rf_rmse]
})
st.dataframe(results)

st.write("R² Score (Linear Regression):", float(lr_r2))
st.write("Direction Accuracy:", float(direction_acc))

# ---------------- TRAIN-TEST VISUAL SPLIT ----------------
st.subheader("Actual vs Predicted (Linear Regression)")
fig, ax = plt.subplots(figsize=(10,5))
ax.plot(y_test_actual, label="Actual Price", linewidth=2)
ax.plot(lr_pred_actual, label="Predicted Price", linestyle="--")
ax.axvline(x=len(y_train), color='black', linestyle=':')
ax.legend()
ax.set_title("Actual vs Predicted Stock Price")
st.pyplot(fig)

# ---------------- CUMULATIVE RETURNS ----------------
st.subheader("Cumulative Returns")
st.line_chart(data["Cumulative Returns"])

# ---------------- FUTURE FORECAST ----------------
last_30 = scaled[-30:]
last_30 = last_30.reshape(1, -1)

future_scaled = lr_model.predict(last_30)
future_price = inverse_close(future_scaled)[0]

st.subheader("Next Day Forecast (Real Price)")
st.write(float(future_price))

# ---------------- CONCLUSION ----------------
st.subheader("Conclusion")
st.write("""
• Volatility captures market risk.
• Rolling window captures short-term memory.
• Random Forest handles non-linear market behavior.
• Direction Accuracy evaluates trend correctness.
• Feature engineering strongly impacts prediction quality.
""")

=======
import numpy as np
import pandas as pd
import yfinance as yf
import streamlit as st
import ta
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor

st.title("📊 Stock Price Forecasting System")
st.markdown("Comparative Analysis of Machine Learning Models for Time-Series Prediction")

# ---------------- SIDEBAR ----------------
st.sidebar.header("Project Info")
st.sidebar.write("Author: Tanisha Patil")
st.sidebar.write("Domain: Time Series Forecasting")
st.sidebar.write("Models Used: Linear Regression, Random Forest")

# ---------------- STOCK SELECTION ----------------
stock = st.selectbox(
    "Select Stock",
    ["TCS.NS", "RELIANCE.NS", "INFY.NS", "AAPL", "^NSEI"]
)

# ---------------- DATA DOWNLOAD ----------------
data = yf.download(stock, start="2018-01-01")

if data.empty:
    st.error("Data not loaded")
    st.stop()

st.subheader("Raw Data Preview")
st.dataframe(data.tail())

# Fix Close
close = data["Close"]
if isinstance(close, pd.DataFrame):
    close = close.iloc[:, 0]

# ---------------- INDICATORS ----------------
data["MA"] = ta.trend.sma_indicator(close, window=14)
data["RSI"] = ta.momentum.rsi(close, window=14)

# 🔥 Volatility Added
data["Volatility"] = data["Close"].rolling(window=14).std()

# Returns + Cumulative Returns
data["Returns"] = data["Close"].pct_change()
data["Cumulative Returns"] = (1 + data["Returns"]).cumprod()

data = data.dropna()

features = data[["Close", "MA", "RSI", "Volatility"]]

# ---------------- HEATMAP ----------------
st.subheader("Feature Correlation Heatmap")
fig_heat, ax_heat = plt.subplots()
sns.heatmap(features.corr(), annot=True, cmap="coolwarm", ax=ax_heat)
st.pyplot(fig_heat)

# ---------------- SCALING ----------------
scaler = MinMaxScaler()
scaled = scaler.fit_transform(features)

# ---------------- ROLLING WINDOW ----------------
X, y = [], []
for i in range(30, len(scaled)):
    X.append(scaled[i-30:i])
    y.append(scaled[i][0])

X, y = np.array(X), np.array(y)

split = int(0.8 * len(X))
X_train, X_test = X[:split], X[split:]
y_train, y_test = y[:split], y[split:]

# ---------------- MODELS ----------------
lr_model = LinearRegression()
lr_model.fit(X_train.reshape(X_train.shape[0], -1), y_train)
lr_pred = lr_model.predict(X_test.reshape(X_test.shape[0], -1))

rf_model = RandomForestRegressor()
rf_model.fit(X_train.reshape(X_train.shape[0], -1), y_train)
rf_pred = rf_model.predict(X_test.reshape(X_test.shape[0], -1))

# ---------------- INVERSE SCALING ----------------
def inverse_close(pred_array):
    temp = np.zeros((len(pred_array), features.shape[1]))
    temp[:, 0] = pred_array
    return scaler.inverse_transform(temp)[:, 0]

y_test_actual = inverse_close(y_test)
lr_pred_actual = inverse_close(lr_pred)
rf_pred_actual = inverse_close(rf_pred)

# ---------------- METRICS ----------------
lr_rmse = np.sqrt(mean_squared_error(y_test_actual, lr_pred_actual))
rf_rmse = np.sqrt(mean_squared_error(y_test_actual, rf_pred_actual))
lr_r2 = r2_score(y_test_actual, lr_pred_actual)

direction_acc = np.mean(
    np.sign(lr_pred_actual[1:] - lr_pred_actual[:-1]) ==
    np.sign(y_test_actual[1:] - y_test_actual[:-1])
)

# ---------------- MODEL COMPARISON ----------------
st.subheader("Model Comparison")
results = pd.DataFrame({
    "Model": ["Linear Regression", "Random Forest"],
    "RMSE (Real Price)": [lr_rmse, rf_rmse]
})
st.dataframe(results)

st.write("R² Score (Linear Regression):", float(lr_r2))
st.write("Direction Accuracy:", float(direction_acc))

# ---------------- TRAIN-TEST VISUAL SPLIT ----------------
st.subheader("Actual vs Predicted (Linear Regression)")
fig, ax = plt.subplots(figsize=(10,5))
ax.plot(y_test_actual, label="Actual Price", linewidth=2)
ax.plot(lr_pred_actual, label="Predicted Price", linestyle="--")
ax.axvline(x=len(y_train), color='black', linestyle=':')
ax.legend()
ax.set_title("Actual vs Predicted Stock Price")
st.pyplot(fig)

# ---------------- CUMULATIVE RETURNS ----------------
st.subheader("Cumulative Returns")
st.line_chart(data["Cumulative Returns"])

# ---------------- FUTURE FORECAST ----------------
last_30 = scaled[-30:]
last_30 = last_30.reshape(1, -1)

future_scaled = lr_model.predict(last_30)
future_price = inverse_close(future_scaled)[0]

st.subheader("Next Day Forecast (Real Price)")
st.write(float(future_price))

# ---------------- CONCLUSION ----------------
st.subheader("Conclusion")
st.write("""
• Volatility captures market risk.
• Rolling window captures short-term memory.
• Random Forest handles non-linear market behavior.
• Direction Accuracy evaluates trend correctness.
• Feature engineering strongly impacts prediction quality.
""")

>>>>>>> ca195d952da0b6fe8ffadda793a857b9990244ce
st.info("Disclaimer: This project is for academic purposes only and not financial advice.")
