import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

info = """You are a homeowner deciding whether you should buy insurance to protect the value of your home in the event of storm damage. Specifically, you have installed a metal roof, and you want to avoid damage from hail. To help you decide, this model simulates the cost of repairs given the probability of a storm, and the conditional probability of hail, given that there is a storm.
"""
st.title("Scenario Modeler")
st.write(info)
st.sidebar.title("Parameters")

nsim = st.sidebar.select_slider("Number of simulations", 
                                list(range(100, 10100, 100)),
                                value=1000
                               )
p_storm = st.sidebar.slider("Probability of storm",
                           value=0.2)
p_hail_given_storm = st.sidebar.slider("Probability of hail given a storm occurs",
                                       value=0.05)
mean_loss = st.sidebar.slider("Expected cost of repairs",
                              min_value=1,
                              max_value=10000)
std_loss = st.sidebar.slider("Std. dev. of cost of repairs",
                             min_value=1,
                             max_value=2500)

def random_loss(mean, std):
    shape = (mean/std)**2
    scale = (std**2)/mean
    return np.random.gamma(shape, scale=scale)

outcomes = [0.]*nsim

for i in range(nsim):
    storm = np.random.binomial(1, p_storm)
    if storm:
        hail = np.random.binomial(1, p_hail_given_storm)
        if hail:
            loss = random_loss(mean_loss, std_loss)
        else:
            loss = 0
    else:
        loss = 0
    outcomes[i] = loss
    
st.write("Expected loss: ${}".format(round(np.mean(outcomes), 2)))
st.write("Std. dev. of losses: ${}".format(round(np.std(outcomes), 2)))
fig, ax = plt.subplots()
sns.kdeplot(outcomes)
st.pyplot(fig)