import matplotlib.pyplot as plt

def plot_price_trend(df, ax=None):
    ax = ax or plt.subplots(figsize=(10,5))[1]
    ax.plot(df['date'], df['close'])
    ax.set_title('MSFT Closing Price Over Time')
    ax.set_ylabel('Adjusted Close')
    return ax

def plot_model_auc(results_df, ax=None):
    ax = ax or plt.subplots(figsize=(8,5))[1]
    results_df.sort_values('test_roc_auc').plot(kind='barh', x='model', y='test_roc_auc', legend=False, ax=ax)
    ax.axvline(.5, linestyle='--')
    ax.set_title('Model Performance Comparison (ROC AUC)')
    return ax
