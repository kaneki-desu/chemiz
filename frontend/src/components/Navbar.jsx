import React from "react";
import { Link } from "react-router-dom";

const Navbar = () => {
  return (
    <nav className="flex justify-center items-center p-4 bg-gray-900">
      <Link
        to="/"
        className="text-white mr-6 hover:text-blue-400 transition-colors"
      >
        Home
      </Link>
      <Link
        to="/history"
        className="text-white hover:text-blue-400 transition-colors"
      >
        History
      </Link>
    </nav>
  );
};

export default Navbar;
