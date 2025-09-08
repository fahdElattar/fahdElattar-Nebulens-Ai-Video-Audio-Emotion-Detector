import angry_person from '../../assets/img/person_angry.jpeg'
import smiling_person from '../../assets/img/person_smiling.png'
import "./Home.css"

const Home = () => {
  
  const handleScroll = (e, sectionId) => {
    e.preventDefault();
    const section = document.getElementById(sectionId);
    section.scrollIntoView({ behavior: 'smooth' });
  };

  return (
    <div className='home' id='Home'>
      <div className="left">
        <img src={angry_person} alt="angry_person" />
      </div>
      <div className="center">
        <h1 className='title'>Emotion Detector</h1>
        <p className='para'>Explore the depths of human emotion with our cutting-edge AI-powered video emotion detection platform</p>
        <a className='select-btn' href="#Process" onClick={(e) => handleScroll(e, 'Process')}><span className='plus'>+</span> Try it now</a>
      </div>
      <div className="right">
        <img src={smiling_person} alt="angry_person" />
      </div>
    </div>
  )
}

export default Home