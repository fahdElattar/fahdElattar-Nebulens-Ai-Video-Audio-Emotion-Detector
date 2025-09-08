import emotions_graph from '../../assets/img/emotions_graph.svg'
import "./Description.css"

const Description = () => {
  return (
    <div className='description' id='Description'>
        <div className="description-desc">
            <h2 className="title">Nebulens : Your Ai Powered Emotion Detector ?</h2>
            <p className='para'>Within the vast expanse of digital content, Nebulens stands as a beacon of emotional , utilizing cutting-edge AI technology to discern and decode seven fundamental human emotions: anger, disgust, fear, happiness, sadness, surprise, and neutrality.</p>
            <p className='para'>Through sophisticated algorithms, Nebulens peers into the visual narratives captured in videos, deciphering the subtle nuances of facial expressions and body language to unveil the emotional tapestry within.</p>
            <p className='para'>Nebulens offers precise insights into human emotions, which is empowering in diverse to deeply understand, engage, and resonate with audiences.</p>
        </div>
        <div className="description-img">
            <img src={emotions_graph} alt="Face detection" />
        </div>
    </div>
  )
}

export default Description