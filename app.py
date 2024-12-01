import streamlit as st

import pandas as pd
import json

from mplsoccer import VerticalPitch
from PIL import Image
import math
st.title("Euros 2024 Players Shot map")

st.subheader("Filter to any team/player to view their shots taken!")
# background_image = Image.open('euro2024_background.jpeg')

df = pd.read_csv("euros_2024_shot_map.csv")

df = df[df['type'] == 'Shot'].reset_index(drop=True)
df['location'] = df['location'].apply(json.loads)

st.sidebar.header("Filter Data")

team = st.sidebar.selectbox("Select a team", df['team'].sort_values().unique(),index = None)

player = st.sidebar.selectbox("Select a player", df[df['team'] == team]['player'].sort_values().unique(), index = None)


def filter_data(df , team, player):
    if team:
        df = df[df['team'] == team]
    if player:
        df = df[df['player'] == player]
    return df


filtered_df = filter_data(df, team, player)


pitch = VerticalPitch(pitch_type='statsbomb', pitch_color='grass', line_color='white' , half=True)

fig,ax = pitch.draw(figsize=(20, 15))
# ax.imshow(background_image, extent=[0, 100, 0, 100], alpha=0.5)


def plot_shots(df, ax, pitch):
    for x in df.to_dict(orient='records'):
        shot_x = float(x['location'][0])
        shot_y = float(x['location'][1])
        goal_x = 100  # assuming the goal is at x=100
        goal_y = 50  # assuming the goal is at y=50
        distance_from_goal = math.hypot(shot_x - goal_x, shot_y - goal_y)
        pitch.scatter(
            x=shot_x,
            y=shot_y,
            ax=ax,
            s=1000 * x['shot_statsbomb_xg'],
            color='green' if x['shot_outcome'] == 'Goal' else 'red',
            edgecolor='black',
            alpha=1 if x['shot_outcome'] == 'Goal' else 0.5,
            zorder=2 if x['type'] == 'Goal' else 1
        )
        ax.annotate(
            f'Distance from goal: {distance_from_goal:.2f} yards',
            xy=(shot_x, shot_y),
            xytext=(shot_x + 5, shot_y + 5),
            textcoords='offset points',
            ha='center',
            va='center',
            fontsize=10,
            color='black'
        )


plot_shots(filtered_df, ax, pitch)

st.pyplot(fig)