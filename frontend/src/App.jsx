import { Route, Routes } from "react-router-dom";
import Navbar from "./components/Navbar";
import Footer from "./components/Footer";
import Home from "./pages/Home";
import About from "./pages/About";
import Services from "./pages/Services";
import Projects from "./pages/Projects";
import Courses from "./pages/Courses";
import Book from "./pages/Book";
import Contact from "./pages/Contact";
import PlagiarismCheck from "./pages/PlagiarismCheck";

export default function App() {
  return (
    <div className="min-h-screen flex flex-col">
      <Navbar />
      <main className="flex-1">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/about" element={<About />} />
          <Route path="/services" element={<Services />} />
          <Route path="/projects" element={<Projects />} />
          <Route path="/courses" element={<Courses />} />
          <Route path="/book" element={<Book />} />
          <Route path="/contact" element={<Contact />} />
          <Route path="/plagiarism-check" element={<PlagiarismCheck />} />
        </Routes>
      </main>
      <Footer />
    </div>
  );
}
