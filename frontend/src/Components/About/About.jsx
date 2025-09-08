import face_detection from '../../assets/img/face_detection.svg'
import "./About.css"

const About = () => {
  return (
    <div className='about' id='About'>
        <div className="about-img">
            <img src={face_detection} alt="Face detection" />
        </div>
        <div className="about-desc">
            <h2 className="title">What is Nebulens ?</h2>
            <p className='para'>Embark on a journey through the cosmos of emotions with our revolutionary AI-driven video emotion detection platform. </p>
            <p className='para'>Nebulens harnesses the power of artificial intelligence to delve into the intricate nuances of facial expressions and body language within videos, offering real-time insights into the emotional landscape of any visual content.</p>
            <p className='para'>From market analysis to content creation and psychological research, Nebulens illuminates the depths of human emotion, empowering users with unparalleled understanding and engagement in the digital realm.</p>
        </div>
    </div>
  )
}

export default About