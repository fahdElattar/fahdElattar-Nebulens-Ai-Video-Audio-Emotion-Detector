import './App.css';
import Navbar from './Components/Navbar';
import Home from './Components/Home';
import Process from './Components/Process';
import About from './Components/About';
import Description from './Components/Description';
import Steps from './Components/Steps';
import Footer from './Components/Footer';
import ScrollButton from './Components/ScrollButton';

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