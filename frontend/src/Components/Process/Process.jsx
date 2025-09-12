import { useState, useEffect } from 'react';
import axios from 'axios';
import "./Process.css"
import '../../styles/App.css';

const Process = () => {
  const [videoFile, setVideoFile] = useState(null);
  const [audioFile, setAudioFile] = useState(null);
  const [inputName, setInputName] = useState("Nothing Selected");
  const [inputType, setInputType] = useState("No Type");
  const [output, setOutput] = useState("");
  const [loading, setLoading] = useState(false);
  const [loadingText, setLoadingText] = useState("Loading");
  const [descriptionText, setDescriptionText] = useState("Please choose your input wisely for Nebulens platform to analyze it to make the final prediction.")
  const [alert, setAlert] = useState(false)
  const [alertText, setAlertText] = useState('')
  const [success, setSuccess] = useState(false)

  useEffect(() => {
    if (loading) {
      const interval = setInterval(() => {
        setLoadingText((prev) => (prev === "Loading..." ? "Loading" : prev + "."));
      }, 500);
      return () => clearInterval(interval);
    } else {
      setLoadingText("Loading");
    }
  }, [loading]);

  useEffect(()=>{
    if(success){
      const timer = setTimeout(()=>{
        setSuccess(false)
      }, 3000)
      return () => clearTimeout(timer)
    }
  }, [success])

  useEffect(() => {
    if(alert){
      const timer = setTimeout(()=>{
        setAlert(false)
      }, 3000)
      return () => clearTimeout(timer)
    }
  }, [alert])

  const handleVideoChange = (e) => {
    if(e.target.files[0]){
      setAudioFile(null);
      setVideoFile(e.target.files[0]);
      setInputName(e.target.files[0].name);
      setInputType(e.target.files[0].type);
    }
  };

  const handleAudioChange = (e) => {
    if(e.target.files[0]){
      setVideoFile(null);
      setAudioFile(e.target.files[0]);
      setInputName(e.target.files[0].name);
      setInputType(e.target.files[0].type);
    }
  };

  const predictVideoEmotion = async (video) => {
    const formData = new FormData();
    formData.append('video', video);

    try {
      const response = await axios.post('http://localhost:5000/predictVideo', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      return response.data.emotion;
    } catch (error) {
      console.error('Error predicting video emotion:', error);
      throw error;
    }
  };

  const predictAudioEmotion = async (audio) => {
    const formData = new FormData();
    formData.append('audio', audio);

    try {
      const response = await axios.post('http://localhost:5000/predictAudio', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      return response.data.emotion;
    } catch (error) {
      console.error('Error predicting audio emotion:', error);
      throw error;
    }
  };

  const handlePredict = async () => {
    if (!audioFile && !videoFile) {
      setAlertText('Please enter a valid input file first!!')
      setAlert(true)
      return;
    }

    setLoading(true);
    try {
      if (audioFile) {
        setOutput('');
        const emotion = await predictAudioEmotion(audioFile);
        setOutput(emotion);
      } else if (videoFile) {
        setOutput('');
        const emotion = await predictVideoEmotion(videoFile);
        setOutput(emotion);
      }
      setSuccess(true)
      setDescriptionText("Your input has been analyzed by Nebulens, revealing a detailed emotional spectrum.The emotion detected is: ")
    } catch (error) {
      setAlert(true)
      setAlertText('Error predicting emotion!!!')
      deletePredict()
    } finally {
      setLoading(false);
    }
  };

  const deletePredict = ()=>{
    setAudioFile(null);
    setVideoFile(null);
    setInputName("Nothing Selected");
    setInputType("No Type");
    setOutput("");
    setDescriptionText("Please choose your input wisely for Nebulens platform to analyze it to make the final prediction.")
  }

  return (
    <div className='process' id="Process">
      <div className={`card alert ${alert ? 'slide-in' : 'slide-out'}`}>
        {alertText}
      </div>
      <div className={`card success ${success ? 'slide-in' : 'slide-out'}`}>
        Your prediction is received successfully!!
      </div>
      <div className="process-img" id='process-img'>

        <input type='file' accept='video/*' className='d-none' id='videoFile' onChange={handleVideoChange} />
        <label htmlFor="videoFile" className='video-label'>Select a video</label>
        
        <input type='file' accept='audio/*' className='d-none' id='audioFile' onChange={handleAudioChange} />
        <label htmlFor="audioFile" className='audio-label'>Select an audio</label>

        {/* <img src={square_bg} alt="Background" /> */}
        
      </div>
      <div className="process-desc">
        <span className="small-title">Your Input</span>
        <h2 className="title">{inputName}</h2>
        <p className='duration'>Type: {inputType}.</p>
        <p className='para'>{descriptionText}<span className='output'>{output}</span>
        </p>
        <div className="action-btns">
          <button className='predict-btn' onClick={handlePredict} disabled={loading}>
            {loading ? loadingText : "Predict"}
          </button>
          {output && (
            <button className='delete-btn' onClick={deletePredict} disabled={loading}>
              Delete
            </button> 
          )}
        </div>
      </div>
    </div>
  );
};

export default Process;
