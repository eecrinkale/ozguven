# AnimeQuotes
🚀Interactive Anime Quote Platform Project with Machine Learning and FastAPI



In this project, I developed a search engine-like FastAPI web platform that dynamically delivers anime quotes based on user interactions. Built using machine learning techniques, this platform provides an interactive experience for anime lovers.

It finds and fetches the anime line that contains the "English" word you enter. and translates it into Turkish by default, you can change it right below if you wish.



Technical Details:



🔍 Artificial Intelligence Model Training:



Libraries: #pandas,#sklearn, #joblib

Features: Pandas for data processing and sklearn for machine learning. TF-IDF vectorizer was implemented for text vectorization. The trained Nearest Neighbors model successfully retrieves citations that closely match user inputs. The model and other components are compressed with joblib.



🔍 API Development:



Libraries: #FastAPI, #slowapi, #GoogleTranslate, #Jinja2

Features: High performance API has been developed with FastAPI. Security and traffic management is provided with Slowapi integration, and citations are instantly translated into Turkish with Google Translate API. With CORS software, seamless interaction from different domains is made possible.



🔍 Interactive Web Interface:



Libraries: #HTML, #CSS, #JS

Features: Basic, Dynamic content delivery, integrated online status controls and response formatting for user interaction.



Platform: https://animequotesml.onrender.com
