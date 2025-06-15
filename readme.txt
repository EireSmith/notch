# Notch

**Notch** is a web application built for freelance creators to efficiently track and visualize their work engagements. It provides insights into average daily pay rates, total and average days worked, and visualizes contract timelines using interactive charts.


---

## 🚀 Features

* 📆 Track freelance job contracts with start and end dates
* 💰 Calculate and display average daily pay rate
* 📊 View total and average days worked
* 📈 Timeline chart of contract start dates using Highcharts
* 🧠 Simple and intuitive UI for easy navigation

---

## 🛠️ Built With

* **Backend:** [Flask](https://flask.palletsprojects.com/)
* **Frontend:** HTML, CSS, JavaScript
* **Data Visualization:** [Highcharts](https://www.highcharts.com/)



## 📈 Highcharts Integration

Highcharts is used to generate a timeline view of contract start dates. Each entry on the chart corresponds to the start of a freelance contract, helping users visualize their work history at a glance.

---

## 🔧 Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/EireSmith/notch.git
   cd notch
   ```

2. **Create a virtual environment**

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   If you encounter installation errors, this could be due to outdated pyyaml.
   pip install pyyaml==5.4.1 --no-build-isolation

   ```

4. **Run the application**

   ```bash
   flask run
   ```

5. **Open in browser**
   Navigate to `http://127.0.0.1:5000/` in your browser.

---

## 📌 Future Improvements
* Displaying invoice previews 
* UI coherence and continuity 
* Hosting on AWS for scalability
* Password reset functionality
---

## 🤝 Contributing

Contributions are welcome! This project is beginner friendly. Please open an issue first to discuss what you would like to change.

1. Fork the repository
2. Create a new branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

## 🙋‍♂️ Author

Created by **Robert Smith (https://github.com/EireSmith)**
If you find this project useful, consider giving it a ⭐️!
**I'd love to collaborate and work with other beginners and learners so please don't hesitate to contribute or request a collaboration from me.**
