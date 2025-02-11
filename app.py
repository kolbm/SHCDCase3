if 'video_id' in locals() and 'start_time' in locals() and 'end_time' in locals():
    video_id, start_time, end_time = video_info
st.markdown(f"""
    <iframe width="560" height="315" 
    src="https://www.youtube.com/embed/{video_id}?start={start_time}&autoplay=1&controls=0" 
    frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe>
""", unsafe_allow_html=True)

import streamlit as st  # Ensure Streamlit is imported

# Introduction button at the top
if st.button("Introduction"):
    st.markdown("""
    At 221B Baker Street we find Holmes just as Dr Watson’s note had described him: listless, unresponsive, oblivious to all around him.
    “He has not resorted to the needle as yet,” whispers Watson. “My plan may keep him from it,” indicating the newspaper clippings in his hand.
    “A tightrope walker at the Royal Italian Circus fell to his death... Foul play suspected... What do you think, Holmes?”
    No answer.
    “‘Society Burglar strikes again’... Hmm, a series of burglaries... Six such over the period June 2nd to June 17th... On July 1st, the seventh occurred at the home of Sir Sanford Leeds... As in the others, no sign of extensive search by the thief and only one piece of jewellery involved... Victims elsewhere at the time. Here’s a complete list of the particulars, Holmes, if you’d care to read it.”
    Silence.
    “Ah, here’s a puzzle... A hansom picked up a fare at its regular stand... The passenger spoke up when he realised that they were heading in the wrong direction but got no answer... Oh, my... The cabbie was dead, still sitting upright in his seat, a knife in his back!... A bobby managed to halt the vehicle... Around the cabbie’s neck was a pouch containing thirty Roman coins, denarii.”
    “The stupid fools!” exclaims Holmes. “If they had allowed the horse to proceed, it would have led them to the scene of the crime! Let me see that, Watson!”
    Watson hands him the clipping and casts a self-satisfied smile in our direction.
    As Holmes, his enthusiasm restored, occupies himself with the clipping, the doorbell rings.
    “I beg you for your help, Mr Holmes,” entreats a tall, bespectacled young man, identifying himself as Gerald Locke.
    “Three days ago, Guy Clarendon was found murdered at Halliday’s. It’s preposterous, but Miss Frances Nolan has been charged and is being detained at Old Bailey.”
    “I was just about to bring the matter to your attention, Holmes,” says Watson, waving another clipping.
    “I cannot believe that she is capable of murder. Even of such a scoundrel as Guy Clarendon.”
    “Scoundrel?” asks Watson. “I’ve only heard very good things about the younger Clarendon. Scion of a wealthy family, an accomplished batsman for the West London Cricketeers, a ranked fencer in international competition—”
    “He was a bounder! Very fond of cards and strong drink and he associated with some rather low East End types. His father had all but disinherited him. I tried to warn Frances that he was only after her money, but to no avail.”
    “Frances and Loretta Nolan,” says Holmes, suddenly stirring to life, “the surviving heirs of Sir Malcolm Nolan, founder of the Aberdeen Navigation Company. Sir Malcolm and Lady Nolan were killed when an avowed anarchist, one Zagreb Yoblinski, threw a bomb into their carriage, mistakenly thinking it carried the Duke of York. Loretta Nolan, aged 4 or 5 at the time, was also in the carriage. Miraculously, she was uninjured. Yes, the gory details of the assassination as well as those of the disposition of a considerable estate were well documented in the newspapers. Mr Locke, you are the suitor for Miss Nolan’s hand, are you not?”
    “Yes,” he admits.
    “Why was Miss Nolan charged with the murder?”
    “Ah, well ....” Locke hesitates. He seems very uncomfortable and removes his spectacles, wiping them as a cover for his distress. Finally in a low, resigned voice he answers, “She was discovered over the body with a pistol in her hand.”
    Holmes nods, takes up the clipping of the cabbie’s death again and turns a deaf ear to Locke’s renewed protestations of Miss Nolan’s innocence. “I’m sorry, Mr Locke,” he says finally, cutting him off, “but I cannot personally take your case. Another very pressing matter has come to my attention.” He goes to retrieve his hat, adding, “You can rest assured, however, that I could not leave you in better hands,” and then he is gone.
    “Ah ... well, Mr Locke,” sputters Dr Watson. “You must excuse... Ah... That is.... As Holmes suggested, we will spare no pains to get at the truth. You have nothing to worry about.”
    “I...I... I’m sure I don’t,” says Locke, sounding rather unconvinced.
    """)
import pandas as pd  # Ensure pandas is imported

# Load introduction section when button is clicked
if st.button("Introduction"):
    st.markdown("""
    **At 221B Baker Street...**  
    Holmes is listless and unresponsive until Watson reads him a series of peculiar cases from the newspaper.  
    Suddenly, the doorbell rings, and Gerald Locke arrives with a desperate plea for Holmes' help.  
    He recounts the case of Miss Frances Nolan, charged with the murder of Guy Clarendon. As Holmes listens, 
    his interest sharpens, and he sets off on what promises to be another thrilling investigation.

    ---
    """)

@st.cache
def load_data():
    return pd.read_csv('your_file.csv')  # Replace 'your_file.csv' with your actual data file

df = load_data()

location_code = st.selectbox("Select Location Code", df['Location Code'].unique())
entry_number = st.number_input("Enter Entry Number", min_value=1, max_value=100, step=1)

result = df[(df['Location Code'] == location_code) & (df['Entry Number'] == entry_number)]

if not result.empty:
    st.subheader("Matching Location")
    st.write(f"<p class='narrative-text'>{result.iloc[0]['Location']}</p>", unsafe_allow_html=True)

    st.subheader("Matching Paragraph")
    st.write(f"<p class='narrative-text'>{result.iloc[0]['Full Text']}</p>", unsafe_allow_html=True)
else:
    st.error("No matching entry found. Please check the Location Code and Entry Number.")

if result is not None and isinstance(result, pd.DataFrame) and not result.empty:
    st.subheader("Matching Location")
    st.write(f"<p class='narrative-text'>{result.iloc[0]['Location']}</p>", unsafe_allow_html=True)

    st.subheader("Matching Paragraph")
    st.write(f"<p class='narrative-text'>{result.iloc[0]['Full Text']}</p>", unsafe_allow_html=True)
else:
    st.error("No matching entry found. Please check the Location Code and Entry Number.")
