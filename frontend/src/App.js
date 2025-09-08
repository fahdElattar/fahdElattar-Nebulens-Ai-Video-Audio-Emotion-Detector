import './styles/App.css';
import './styles/responsiveness.css';
import './styles/reusable.css';

import About from './Components/About/About';
import Description from './Components/Description/Description';
import Footer from './Components/Footer/Footer';
import Home from './Components/Home/Home';
import Navbar from './Components/Navbar/Navbar';
import Process from './Components/Process/Process';
import ScrollButton from './Components/ScrollButton/ScrollButton';
import Steps from './Components/Steps/Steps';


function App() {
  return (
    <div className='container'>
      <Navbar />
      <Home />
      <Process />
      <About />
      <Description />
      <Steps />
      <Footer />
      <ScrollButton />
    </div>
  );
}

export default App;