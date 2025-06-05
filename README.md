# Hornbill4U 🦜

**Hornbill4U** is a comprehensive web application designed to provide an interactive platform for hornbill habitat suitability analysis and conservation management. This project serves as the frontend interface for the advanced machine learning-based habitat modeling system, making hornbill conservation data accessible to researchers, conservationists, and the general public.

## 🌟 Overview

Hornbill4U bridges the gap between complex ecological data and user-friendly visualization, offering an intuitive web interface for exploring hornbill habitat predictions, movement patterns, and conservation insights. The application integrates real-time data from various sources including satellite imagery, climate data, and citizen science observations.

## ✨ Features

### 🗺️ Interactive Habitat Mapping
- **Real-time Habitat Suitability Maps**: Visualize predicted suitable habitats across different regions
- **Layered Geographic Information**: Toggle between different environmental layers (NDVI, climate, elevation)
- **Zoom and Navigation**: Seamless map exploration with location-based searches

### 📊 Data Visualization Dashboard
- **Movement Pattern Analysis**: Interactive charts showing hornbill tracking data and migration routes
- **Environmental Factor Analysis**: SHAP-based feature importance plots and correlation matrices
- **Temporal Trends**: Time-series visualization of habitat changes and species observations

### 🔍 Advanced Search & Filtering
- **Species-Specific Analysis**: Filter data by hornbill species (Great Hornbill, Wreathed Hornbill)
- **Geographic Filtering**: Search by state, district, or protected area
- **Date Range Selection**: Analyze data across different time periods

### 📈 Conservation Analytics
- **Priority Area Identification**: Highlight critical conservation zones
- **Threat Assessment**: Visualize habitat fragmentation and human impact
- **Success Stories**: Showcase conservation achievements and case studies

### 🌐 Citizen Science Integration
- **Observation Submission**: Allow users to contribute hornbill sightings
- **Data Validation**: Community-based verification of observations
- **Educational Resources**: Learning materials about hornbill ecology and conservation

### 📱 Responsive Design
- **Mobile-Friendly Interface**: Optimized for smartphones and tablets
- **Cross-Browser Compatibility**: Works seamlessly across different web browsers
- **Accessibility Features**: Screen reader support and keyboard navigation

## 🛠️ Technologies Used

### Backend
- **Python 3.8+**: Core programming language
- **Flask**: Lightweight web framework for API development
- **SQLAlchemy**: Database ORM for data management
- **Pandas & NumPy**: Data processing and analysis
- **Scikit-learn**: Machine learning integration
- **Folium**: Interactive map generation

### Frontend
- **HTML5**: Semantic markup structure
- **CSS3**: Modern styling with Flexbox and Grid
- **JavaScript (ES6+)**: Interactive functionality and API calls
- **Bootstrap 5**: Responsive design framework
- **Chart.js**: Data visualization library
- **Leaflet.js**: Interactive mapping library

### Data & APIs
- **Google Earth Engine**: Satellite imagery processing
- **OpenWeather API**: Real-time climate data
- **Movebank API**: Animal tracking data integration
- **eBird API**: Citizen science observation data

## 🚀 Installation

### Prerequisites
```bash
Python 3.8 or higher
Git
```

### Step-by-Step Setup

1. **Clone the repository:**
```bash
git clone https://github.com/vishals25/Hornbill4U.git
cd Hornbill4U
```

2. **Create and activate a virtual environment:**
```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. **Install required packages:**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables:**
```bash
# Create a .env file in the root directory
touch .env

# Add the following variables:
FLASK_SECRET_KEY=your-secret-key-here
GOOGLE_EARTH_ENGINE_KEY=your-gee-key
OPENWEATHER_API_KEY=your-weather-api-key
DATABASE_URL=sqlite:///hornbill4u.db
```

5. **Initialize the database:**
```bash
python init_db.py
```

6. **Run the application:**
```bash
python app.py
```

7. **Access the application:**
Open your browser and navigate to `http://localhost:5000/`

## 🎯 Usage Guide

### For Researchers
1. **Access Data Dashboard**: Navigate to `/dashboard` for comprehensive analytics
2. **Download Datasets**: Export processed data for further analysis
3. **Model Integration**: Use API endpoints to integrate with custom models

### For Conservationists
1. **Identify Priority Areas**: Use habitat suitability maps to focus conservation efforts
2. **Monitor Threats**: Track habitat fragmentation and human impact
3. **Plan Interventions**: Access species-specific conservation recommendations

### For Educators
1. **Interactive Learning**: Use species profiles and educational resources
2. **Classroom Integration**: Embed maps and visualizations in presentations
3. **Student Projects**: Provide data access for research projects

### For Citizen Scientists
1. **Submit Observations**: Contribute hornbill sightings through the portal
2. **Validate Data**: Help verify community-submitted observations
3. **Track Impact**: See how contributions support conservation efforts

## 🧪 Testing

Run the test suite:
```bash
# Run all tests
python -m pytest tests/

# Run specific test file
python -m pytest tests/test_app.py

# Run with coverage
python -m pytest --cov=app tests/
```

## 🚀 Deployment

### Local Development
```bash
export FLASK_ENV=development
python app.py
```

### Production Deployment
```bash
# Using Gunicorn
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 app:app

# Using Docker
docker build -t hornbill4u .
docker run -p 5000:5000 hornbill4u
```

### Environment Variables for Production
```bash
FLASK_SECRET_KEY=production-secret-key
DATABASE_URL=postgresql://user:password@localhost/hornbill4u
GOOGLE_EARTH_ENGINE_KEY=production-gee-key
OPENWEATHER_API_KEY=production-weather-key
```

## 🤝 Contributing

We welcome contributions from the community! Please follow these guidelines:

### Development Team
- **Vishal S** - Lead Developer, UI/UX Design
- **Dines S** - Frontend Development, API Integration
- **Aneesh V** - Frontend Development, Data Visualization
- **Anish M** - Database Management, Testing

*Department of Computer Science and Engineering*  
*Coimbatore Institute of Technology, Coimbatore, India*

### How to Contribute

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Make your changes**: Follow coding standards and add tests
4. **Commit your changes**: `git commit -m 'Add amazing feature'`
5. **Push to the branch**: `git push origin feature/amazing-feature`
6. **Open a Pull Request**: Describe your changes and their impact

### Contribution Guidelines
- Follow PEP 8 style guide for Python code
- Use semantic HTML and modern CSS practices
- Write comprehensive tests for new features
- Update documentation for any API changes
- Ensure responsive design compatibility

### Areas for Contribution
- **Mobile App Development**: React Native or Flutter implementation
- **Advanced Analytics**: Machine learning model improvements
- **Internationalization**: Multi-language support
- **Performance Optimization**: Database and frontend optimization
- **Security Enhancements**: Authentication and authorization improvements

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

### License Summary
- ✅ Commercial use
- ✅ Modification
- ✅ Distribution
- ✅ Private use

## 🙏 Acknowledgments

### Research Collaboration
- **Salim Ali Centre for Ornithology and Natural History** - Ecological expertise and data validation
- **Dr. Rohit Naniwadekar** - Hornbill telemetry data and research insights
- **Coimbatore Institute of Technology** - Academic support and resources

### Data Sources
- **Citizen Science Community** - eBird, iNaturalist, and MoveBird contributors
- **Google Earth Engine** - Satellite imagery and geospatial analysis
- **OpenWeather** - Real-time environmental data
- **Movebank** - Animal tracking data repository

### Technical Support
- **Flask Community** - Web framework development
- **Leaflet.js Contributors** - Interactive mapping capabilities
- **Chart.js Team** - Data visualization tools
- **Bootstrap Team** - Responsive design framework

## 📞 Contact & Support

### Development Team
- **Email** : 71762205016@cit.edu.in,71762205006@cit.edu.in,71762205007@cit.edu.in,71762205062@cit.edu.in
- **GitHub**: [Hornbill4U Repository](https://github.com/vishals25/Hornbill4U)
- **Issues**: [Report bugs or request features](https://github.com/vishals25/Hornbill4U/issues)

### Academic Contact
- **Institution**: Coimbatore Institute of Technology
- **Department**: Computer Science and Engineering
- **Location**: Coimbatore, Tamil Nadu, India

### Community
- **Slack Channel**: #hornbill4u-support
- **Discord Server**: Hornbill4U Community
- **Mailing List**: Subscribe for updates and announcements

---

## 🌍 Impact & Future Vision

Hornbill4U represents a significant step forward in digital conservation technology. By making complex ecological data accessible through an intuitive web interface, we're empowering:

- **Researchers** to make data-driven conservation decisions
- **Conservationists** to optimize resource allocation
- **Educators** to engage students with real-world environmental challenges
- **Citizens** to participate meaningfully in conservation efforts

### Future Roadmap
- **Mobile Application**: Native iOS and Android apps
- **AI Integration**: Advanced machine learning predictions
- **Community Features**: User profiles and collaboration tools
- **Real-time Alerts**: Habitat threat notification system
- **Multi-species Support**: Expand beyond hornbills to other wildlife

*Together, we can make a difference in hornbill conservation through technology and community action.*

---

**Made with ❤️ for hornbill conservation**
