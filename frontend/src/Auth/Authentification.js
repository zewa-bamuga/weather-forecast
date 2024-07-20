import React, {useState} from 'react';
import {useNavigate} from 'react-router-dom';
import styles from './Authentification.module.css';
import Rectangle from './Rectangle';
import axios from 'axios';

export default function AuthenticationForm() {
    const [username, setUsername] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [isLoggedIn, setIsLoggedIn] = useState(false);
    const [error, setError] = useState(null);
    const [showRectangle, setShowRectangle] = useState(false);
    const [showPassword, setShowPassword] = useState(false);
    const navigate = useNavigate();

    const handleTogglePasswordVisibility = () => {
        setShowPassword(!showPassword);
    };

    const handleInputChange = (e, setValue) => {
        setValue(e.target.value);
    };

    const handleSubmit = async (e) => {
        e.preventDefault();

        console.log('handleSubmit triggered');

        try {
            console.log('Sending request to server');

            const response = await axios.post('http://localhost:8000/api/authentication/v1/authentication', {
                username,
                email,
                password,
            });

            console.log('Response received from server', response.data);

            const {accessToken} = response.data;
            localStorage.setItem('tokenData', JSON.stringify({token: accessToken}));

            console.log('Вы успешно вошли в систему!');

            navigate('/menu');
            setIsLoggedIn(true);
        } catch (error) {
            console.error('Ошибка входа:', error.response ? error.response.data : 'Сервер не ответил');
            setError('Неправильный логин или пароль');
            setShowRectangle(true);
            setTimeout(() => setShowRectangle(false), 4000);
        }

        setUsername('');
        setEmail('');
        setPassword('');
    };

    return (
        <div className={styles.registrationContainer}>
            <form className={styles.registrationForm} onSubmit={handleSubmit}>
                <h1 className={styles.registrationTitle}>Вход в приложение Погода</h1>
                <input
                    type="text"
                    value={username}
                    onChange={(e) => handleInputChange(e, setUsername)}
                    placeholder="Username"
                    className={styles.inputField}
                />
                <input
                    type="text"
                    value={email}
                    onChange={(e) => handleInputChange(e, setEmail)}
                    placeholder="Почта"
                    className={styles.inputField}
                />
                <br/>
                <input
                    type={showPassword ? 'text' : 'password'}
                    value={password}
                    onChange={(e) => handleInputChange(e, setPassword)}
                    placeholder="Пароль"
                    className={`${styles.inputField} ${styles.passwordField}`}
                />
                <button
                    type="button"
                    onClick={handleTogglePasswordVisibility}
                    className={styles.passwordVisibilityButton}
                >
                    {showPassword ? 'Hide' : 'Show'}
                </button>
                <br/>
                {error && (
                    <div className={styles.errorContainer}>
                        <p className={styles.errorMessage}>{error}</p>
                    </div>
                )}
                <button type="submit" className={styles.submitButton}>
                    Войти
                </button>
                <span className={styles.agreementText} type="last_agree">
                    При входе вы принимаете условия
                    <a href="https://disk.yandex.ru/i/w9SBr8X7PzHhUw" target="_blank" className={styles.link}>
                        публичной оферты
                    </a>
                    <span className={styles.andSpacer}> и</span>
                    <a href="https://disk.yandex.ru/i/w9SBr8X7PzHhUw" target="_blank" className={styles.link}>
                        политики обработки персональных данных
                    </a>
                </span>
                <hr className={styles.hrLine}/>
                <label className={styles.labelText} type="acc">
                    Нет аккаунта?{' '}
                    <span onClick={() => navigate('/RegistrationForm')} className={styles.linkText} type="reg">
                        Зарегистрироваться
                    </span>
                </label>
            </form>
            {showRectangle &&
                <Rectangle text="Ошибка входа"/>}
        </div>
    );
}
