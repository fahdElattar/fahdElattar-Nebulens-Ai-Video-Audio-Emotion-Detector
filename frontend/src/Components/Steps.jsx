import React from 'react'

const Steps = () => {

  const handleScroll = (e, sectionId) =>{
    e.preventDefault()
    const section = document.getElementById(sectionId)
    section.scrollIntoView({behavior: 'smooth'})
  }

  return (
    <div className='steps' id='Steps'>
        <div className="header">
            <h3 className='small-title'>Nebulens</h3>
            <h2 className='title'>How it Works</h2>
        </div>
        <div className="body">
            <div className="card">
                <div className="card-header">
                    <span className="number">01</span>
                </div>
                <div className="card-body">
                    <h3 className="card-name">Upload</h3>
                    <p className="card-desc">Start by uploading your file onto the our platform. Choose your video carefully and make sure it's 5 seconds or less.</p>
                </div>
                </div>
            <div className="card">
                <div className="card-header">
                    <span className="number">02</span>
                </div>
                <div className="card-body">
                    <h3 className="card-name">Process</h3>
                    <p className="card-desc">Once uploaded, our AI model meticulously analyzes every frame of your file, deciphering the emotions expressed in it.</p>
                </div>
            </div>
            <div className="card">
                <div className="card-header">
                    <span className="number">03</span>
                </div>
                <div className="card-body">
                    <h3 className="card-name">Review</h3>
                    <p className="card-desc">Once the analysis is complete, you'll receive a detailed report outlining the emotions detected throughout your file.</p>
                </div>
            </div>
        </div>
        <div className="steps-footer">
            <a href='#Process' className='try-btn' onClick={(e)=> handleScroll(e, 'Process')}>Try it now</a>
        </div>
    </div>
  )
}

export default Steps