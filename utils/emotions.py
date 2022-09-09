import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
from utils.general import is_loc_max_or_end

emotinos_names = ['angry','disgusted','afraid','happy','neutral','sad','surprised']

def show_strongest_emotion(emotions):
    strongest_emotion={"Emotion":"angry", "Perc": 0}
    for emotion in emotinos_names:
        perc=round(emotions[emotion].mean()*100)
        if strongest_emotion["Perc"]<perc:
            strongest_emotion["Perc"]=perc
            strongest_emotion["Emotion"]=emotion
    st.header(f'You seemed mostly **{strongest_emotion["Emotion"]}** ({strongest_emotion["Perc"]}%).\n')

def most_emotional_face(emotion, result):
    emotion_index=emotinos_names.index(emotion)
    index_most=0
    perc_most=0
    for i, v in enumerate(result["Emotions"]):
        if v[emotion_index]>perc_most:
            perc_most=v[emotion_index]
            index_most=i
    return result["Frames"][index_most]

def show_emotion_perc(emotions):
    for emotion in emotinos_names:
        perc=round(emotions[emotion].mean()*100)
        st.write(f"You were **{perc}%** {emotion}.\n")

def emotion_colour(emotion):
    if emotion is "neutral":
        return "black"
    if emotion is "happy":
        return "green"
    return "red"

def show_emotion_graph(emotions, result):
    no_columns=3

    #Strongest emotions
    strongest_emotions=emotinos_names[0:no_columns]
    for emotion in emotinos_names:
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


    st.markdown(f"You also seemed quite **{strongest_emotions[1]}** and **{strongest_emotions[2]}**.")
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
            columns[i].write(f"You were **{round(emotions[emotion].mean()*100)}%** {emotion}.")
            columns[i].write(f"This is your most {emotion} face:")

            #Image
            image=most_emotional_face(emotion, result)
            columns[i].image(image, channels="BGR")

            #Next column
            i+=1
