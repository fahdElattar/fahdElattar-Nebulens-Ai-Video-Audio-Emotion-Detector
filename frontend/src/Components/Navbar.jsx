import React from 'react'
import galaxy_icon from '../assets/img/galaxy_icon.svg'

const Navbar = () => {
  
  const handleScroll = (e, sectionId) => {
    e.preventDefault();
    const section = document.getElementById(sectionId);
    section.scrollIntoView({ behavior: 'smooth' });
  };

  return (
    <div className='navbar' id='Navbar'>
        <div className="logo-section">
            <img src={galaxy_icon} alt="Nebulens-Logo" className='logo-icon'/>
            <p className='logo-name'>Nebu<span className='purple-name'>lens</span></p>
        </div>
        <ul className='links-section'>
            <li><a href="#Navbar" onClick={(e)=> handleScroll(e, 'Navbar')}>Home</a></li>
            <li><a href="#About" onClick={(e)=> handleScroll(e, 'About')}>About</a></li>
            <li><a href="#Description" onClick={(e)=> handleScroll(e, 'Description')}>Description</a></li>
            <li><a href="#Steps" onClick={(e)=> handleScroll(e, 'Steps')}>Steps</a></li>
        </ul>
    </div>
  )
}

export default Navbar