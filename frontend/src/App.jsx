import { useEffect, useState } from "react";
import axios from "axios";

function App() {
  const [medicines, setMedicines] = useState([]);
  const [search, setSearch] = useState("");
  const [result, setResult] = useState(null);

  useEffect(() => {
    fetchMedicines();
  }, []);

  const fetchMedicines = async () => {
    try {
      const res = await axios.get(
        "http://127.0.0.1:8000/all-medicines"
      );
      setMedicines(res.data);
    } catch (error) {
      console.error(error);
    }
  };

  const searchMedicine = async () => {
    try {
      const response = await fetch(
        `http://127.0.0.1:8000/search-medicine/${search}`
      );

      const data = await response.json();
      setResult(data);
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <div style={{ padding: "20px" }}>
      <h1>Pharmacy Management System</h1>

      <h2>Search Medicine</h2>

      <div style={{ marginBottom: "20px" }}>
        <input
          type="text"
          placeholder="Enter Medicine Name"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          style={{
            padding: "10px",
            marginRight: "10px",
            width: "250px",
          }}
        />

        <button
          onClick={searchMedicine}
          style={{
            padding: "10px 20px",
            cursor: "pointer",
          }}
        >
          Search
        </button>
      </div>

      {result && result.name && (
        <div
          style={{
            border: "1px solid black",
            padding: "15px",
            marginBottom: "20px",
            width: "400px",
          }}
        >
          <h3>Medicine Found</h3>

          <p><b>Name:</b> {result.name}</p>
          <p><b>Quantity:</b> {result.quantity}</p>
          <p><b>Price:</b> ₹{result.price}</p>
          <p><b>Expiry Date:</b> {result.expiry_date}</p>
          <p><b>Manufacturer:</b> {result.manufacturer}</p>
        </div>
      )}

      <h2>All Medicines</h2>

      <table border="1" cellPadding="10">
        <thead>
          <tr>
            <th>Name</th>
            <th>Quantity</th>
            <th>Price</th>
            <th>Expiry Date</th>
            <th>Manufacturer</th>
          </tr>
        </thead>

        <tbody>
          {medicines.map((med, index) => (
            <tr key={index}>
              <td>{med.name}</td>
              <td>{med.quantity}</td>
              <td>{med.price}</td>
              <td>{med.expiry_date}</td>
              <td>{med.manufacturer}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default App;