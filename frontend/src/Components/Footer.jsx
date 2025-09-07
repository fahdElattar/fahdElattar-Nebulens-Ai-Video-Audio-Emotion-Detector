import React from 'react'
import galaxy_icon from '../assets/img/galaxy_icon.svg'

const Footer = () => {
  return (
    <div className='footer'>
        <p className="rights">&copy; 2024 All Rights Reserved</p>
        <div className="logo-section">
            <img src={galaxy_icon} alt="Nebulens-Logo" className='logo-icon'/>
            <p className='logo-name'>Nebu<span className='purple-name'>lens</span></p>
        </div>
        <p className="design">Designed By Fahd El Attar</p>
    </div>
  )
}

export default Footer