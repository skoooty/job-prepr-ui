import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from utils.general import is_loc_max_or_end


emotions_names = ['angry','disgusted','afraid','happy','neutral','sad','surprised']

def show_strongest_emotion(emotions):
    strongest_emotion={"Emotion":"angry", "Perc": 0}
    for emotion in emotions_names:
        perc=emotions[emotion].mean()*100
        if strongest_emotion["Perc"]<perc:
            strongest_emotion["Perc"]=perc
            strongest_emotion["Emotion"]=emotion
    st.markdown(f'<h2 style=text-align:left;>You seemed mostly <b>{strongest_emotion["Emotion"]}<b> ({round(strongest_emotion["Perc"])}%).</h5>', unsafe_allow_html=True)

def most_emotional_face(emotion, emotions_list, frames):

    emotion_index=emotions_names.index(emotion)
    index_most=0
    perc_most=0
    for i, v in enumerate(emotions_list):
        if v[emotion_index]>perc_most:
            perc_most=v[emotion_index]
            index_most=i
    if type(frames[index_most]) == list:
        return np.array(frames[index_most])
    return frames[index_most]

def show_emotion_perc(emotions):
    for emotion in emotions_names:
        perc=round(emotions[emotion].mean()*100)
        st.markdown(f"<p style=text-align:left;>You were <b>{perc}%</b> {emotion}.</p>", unsafe_allow_html=True)

def emotion_colour(emotion):
    if emotion is "neutral":
        return "black"
    if emotion is "happy":
        return "green"
    return "red"

def show_emotion_graph(emotions, emotions_list, frames=None, images=None):
    no_columns=3

    #Strongest emotions
    strongest_emotions=emotions_names[0:no_columns]
    for emotion in emotions_names:
        for index, strong_emotion in enumerate(strongest_emotions):
            if emotions[emotion].mean()>emotions[strong_emotion].mean() and emotion not in strongest_emotions:
                strongest_emotions[index]=emotion

    #Sorting strongest emotions + resizing
    for i, strong_emotion1 in enumerate(strongest_emotions):
        for j, strong_emotion2 in enumerate(strongest_emotions):
            if i<j:
                if emotions[strong_emotion1].mean()<emotions[strong_emotion2].mean():
                    k=strongest_emotions[i]
                    strongest_emotions[i]=strongest_emotions[j]
                    strongest_emotions[j]=k


    st.markdown(f"<h4 style=text-align:left;>You also seemed quite <b>{strongest_emotions[1]}</b> and <b>{strongest_emotions[2]}</b>. </p>", unsafe_allow_html=True)
    columns = st.columns(no_columns)

    #Displaying
    i=0
    images_list = []
    for emotion in strongest_emotions:
        if i<no_columns:
            #Subtitle
            columns[i].subheader(emotion)

            #Graph

            fig = plt.figure(figsize=(10, 12), facecolor='#EDF2F4')

            ax = fig.add_axes([0, 0, 1, 1])
            ax.axis('off')
            plt.ylim([-5, 120])

            sns.lineplot(data=emotions[emotion]*100, color="black")

            #X axis
            Xs=[]
            Ys=[]
            Ys_mean=[]
            for j in range(len(emotions[emotion])):
                Xs.append(j)
                Ys.append(0)
                Ys_mean.append(emotions[emotion].mean()*100)
            sns.lineplot(y=Ys, x=Xs, color="gray")
            sns.lineplot(y=Ys_mean, x=Xs, color="blue")
            if emotions[emotion].mean()*100 <10:
                plt.text(x = len(emotions[emotion]),
                                    y = emotions[emotion].mean()*100,
                                    s = 'Ø {:.0f}'.format(emotions[emotion].mean()*100) + " %  ",
                                    color = "blue", size=40)
            else:
                plt.text(x = len(emotions[emotion]),
                                    y = emotions[emotion].mean()*100,
                                    s = 'Ø {:.0f}'.format(emotions[emotion].mean()*100) + " %",
                                    color = "blue", size=40)


            #Label points on the plot
            how_often=len(Xs)//3
            lastx=-10
            lasty=-10
            for x, y in zip(Xs, emotions[emotion]*100):
                if is_loc_max_or_end(x, list(emotions[emotion]*100)):
                    if (x-lastx>how_often or abs(lasty-y)>30) and y>emotions[emotion].mean()*100+10:
                        plt.text(x = x-1, y = y+3, s = '{:.0f}'.format(y) + " %",
                                color = "black", size=40)
                        lastx=x
                        lasty=y

            #Display graph
            columns[i].pyplot(fig)

            #Text

            columns[i].markdown(f"<p style=text-align:left;>You were <b>{round(emotions[emotion].mean()*100)}%</b> {emotion}.</p>", unsafe_allow_html=True)
            columns[i].markdown(f"<p style=text-align:left;>Your most {emotion} face:</p>", unsafe_allow_html=True)


            #Image
            if images is None:
                image=most_emotional_face(emotion, emotions_list, frames)
                images_list.append(image.tolist())
            else:
                image=np.array(images[i])
            columns[i].image(image, channels="BGR")

            #Next column
            i+=1
    return images_list

def show_emotion_graph_wo_photos(emotions):
    no_columns=3

    #Strongest emotions
    strongest_emotions=emotions_names[0:no_columns]
    for emotion in emotions_names:
        for index, strong_emotion in enumerate(strongest_emotions):
            if emotions[emotion].mean()>emotions[strong_emotion].mean() and emotion not in strongest_emotions:
                strongest_emotions[index]=emotion

    #Sorting strongest emotions + resizing
    for i, strong_emotion1 in enumerate(strongest_emotions):
        for j, strong_emotion2 in enumerate(strongest_emotions):
            if i<j:
                if emotions[strong_emotion1].mean()<emotions[strong_emotion2].mean():
                    k=strongest_emotions[i]
                    strongest_emotions[i]=strongest_emotions[j]
                    strongest_emotions[j]=k


    st.markdown(f"<p style=text-align:left;>You also seemed quite <b>{strongest_emotions[1]}</b> and <b>{strongest_emotions[2]}</b>.</p>", unsafe_allow_html=True)
    columns = st.columns(no_columns)

    #Displaying
    i=0
    for emotion in strongest_emotions:
        if i<no_columns:
            #Subtitle
            columns[i].subheader(emotion)

            #Graph
            fig = plt.figure(figsize=(10, 10))
            ax = fig.add_axes([0, 0, 1, 1])
            ax.axis('off')
            plt.ylim([0, 100])

            sns.lineplot(data=emotions[emotion]*100, color="black")

            #X axis
            Xs=[]
            Ys=[]
            Ys_mean=[]
            for j in range(len(emotions[emotion])):
                Xs.append(j)
                Ys.append(0)
                Ys_mean.append(emotions[emotion].mean()*100)
            sns.lineplot(y=Ys, x=Xs, color="gray")
            sns.lineplot(y=Ys_mean, x=Xs, color="blue")
            plt.text(x = len(emotions[emotion]),
                                y = emotions[emotion].mean()*100,
                                s = 'Ø {:.0f}'.format(emotions[emotion].mean()*100) + " %",
                                color = "blue", size=40)


            #Label points on the plot
            how_often=len(Xs)//3
            lastx=-10
            lasty=-10
            for x, y in zip(Xs, emotions[emotion]*100):
                if is_loc_max_or_end(x, list(emotions[emotion]*100)):
                    if (x-lastx>how_often or abs(lasty-y)>30) and y>emotions[emotion].mean()*100+10:
                        plt.text(x = x-1, y = y+3, s = '{:.0f}'.format(y) + " %",
                                color = "black", size=40)
                        lastx=x
                        lasty=y

            #Display graph
            columns[i].pyplot(fig)

            #Text
            columns[i].markdown(f"<p style=text-align:left;>You were <b>{round(emotions[emotion].mean()*100)}%</b> {emotion}.</p>", unsafe_allow_html=True)
            #Next column
            i+=1
