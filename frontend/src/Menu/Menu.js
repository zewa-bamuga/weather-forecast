import React, {useState, useEffect} from 'react';
import styles from './Menu.module.css';
import axios from 'axios';

export default function Menu() {
    const [username, setUsername] = useState('');
    const [city, setCity] = useState('');
    const [weatherData, setWeatherData] = useState(null);
    const [searchHistory, setSearchHistory] = useState({});
    const [cityes, setCityes] = useState([]);

    useEffect(() => {
        const fetchUsername = async () => {
            const token = JSON.parse(localStorage.getItem('tokenData'))?.token;
            if (!token) {
                console.error('Token is missing');
                return;
            }

            try {
                const response = await axios.get('http://localhost:8000/api/profile/v1/me', {
                    headers: {
                        'token': token
                    }
                });
                setUsername(response.data.username);
            } catch (error) {
                console.error('Error fetching username:', error.message || error);
            }
        };

        fetchUsername();
    }, []);

    const fetchCityWeather = async (selectedCity) => {
        const token = JSON.parse(localStorage.getItem('tokenData'))?.token;
        if (!token) {
            console.error('Token is missing');
            return;
        }

        try {
            const response = await axios.post('http://localhost:8000/api/meteo/v1/weather', null, {
                headers: {
                    'token': token
                },
                params: {
                    city: selectedCity
                }
            });
            setWeatherData(response.data);
        } catch (error) {
            console.error('Error fetching weather:', error.message || error);
        }
    };

    const fetchSearchHistory = async () => {
        const token = JSON.parse(localStorage.getItem('tokenData'))?.token;
        if (!token) {
            console.error('Token is missing');
            return;
        }

        try {
            const response = await axios.get('http://localhost:8000/api/meteo/v1/list', {
                headers: {
                    'token': token
                }
            });
            setSearchHistory(response.data);
        } catch (error) {
            console.error('Error fetching search history:', error.message || error);
        }
    };

    const fetch5_cityes = async () => {
        const token = JSON.parse(localStorage.getItem('tokenData'))?.token;
        if (!token) {
            console.error('Token is missing');
            return;
        }

        try {
            const response = await axios.get('http://localhost:8000/api/meteo/v1/5_cityes', {
                headers: {
                    'token': token
                }
            });
            setCityes(response.data.items); // исправлено для использования "items"
        } catch (error) {
            console.error('Error fetching 5 cityes:', error.message || error);
        }
    };

    useEffect(() => {
        fetchSearchHistory();
        fetch5_cityes();
    }, []);

    const handleInputChange = (event) => {
        setCity(event.target.value);
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        fetchCityWeather(city);
    };

    const handleCityClick = (cityName) => {
        fetchCityWeather(cityName);
    };

    return (
        <div className={styles.outerContainer}>
            <div className={styles.leftContainer}>
                <form className={styles.leftLCForm}>
                    <h3 className={styles.LCTitleCount}>Счетчик просмотров</h3>
                    {Object.entries(searchHistory).map(([city, count]) => (
                        <div key={city} className={styles.cityCount}>
                            <a><span>{city}:</span> <span>{count}</span></a>
                        </div>
                    ))}
                </form>
            </div>
            <div className={styles.container}>
                <form className={styles.LCForm} onSubmit={handleSubmit}>
                    <h1 className={styles.LCTitle}>{username}, введите город, в котором хотите посмотреть погоду на
                        сегодня!</h1>
                    <input
                        type="text"
                        value={city}
                        onChange={handleInputChange}
                        placeholder="Ваш город"
                        className={styles.searchField}
                    />
                    <button type="submit" className={styles.submitButton}>Посмотреть погоду</button>
                    {weatherData && (
                        <div className={styles.weatherContainer}>
                            <table className={styles.weatherTable}>
                                <thead>
                                <tr>
                                    <th>Время</th>
                                    <th>Температура (°C)</th>
                                    <th>Влажность (%)</th>
                                    <th>Скорость ветра (м/с)</th>
                                </tr>
                                </thead>
                                <tbody>
                                {weatherData.time.map((time, index) => (
                                    <tr key={index}>
                                        <td>{new Date(time).toLocaleTimeString([], {
                                            hour: '2-digit',
                                            minute: '2-digit'
                                        })}</td>
                                        <td>{weatherData.temperature2M[index]}</td>
                                        <td>{weatherData.relativeHumidity2M[index]}</td>
                                        <td>{weatherData.windSpeed10M[index]}</td>
                                    </tr>
                                ))}
                                </tbody>
                            </table>
                        </div>
                    )}
                </form>
            </div>
            <div className={styles.fixedContainer}>
                <h3 className={styles.rightLCTitle}>Смотрели ранее</h3>
                {cityes.map((cityItem) => (
                    <button
                        key={cityItem.city}
                        className={styles.historyCount}
                        onClick={() => handleCityClick(cityItem.city)}
                    >
                        {cityItem.city}
                    </button>
                ))}
            </div>
        </div>
    );
}
