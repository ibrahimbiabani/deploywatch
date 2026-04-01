import axios from "axios";

async function loadDeployments() {
  const { data } = await axios.get("/deployments");
  const tbody = document.querySelector("#deployments tbody");
  tbody.innerHTML = "";
  for (const d of data) {
    const row = document.createElement("tr");
    row.innerHTML = `<td>${d.service}</td><td>${d.version}</td><td>${d.env}</td><td>${d.status}</td>`;
    tbody.appendChild(row);
  }
}

loadDeployments();
