import React, {useState} from 'react';
import axios from 'axios';
import {useNavigate} from 'react-router-dom';
import styles from './RegistrationForm.module.css';

export default function RegistrationForm() {
    const [username, setUsername] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');

    const navigate = useNavigate();

    const handleInputChange = (event, setterFunction) => {
        setterFunction(event.target.value);
    };

    const handleSubmit = async (event) => {
        event.preventDefault();

        try {
            const response = await axios.post('http://localhost:8000/api/authentication/v1/registration', {
                username,
                email,
                password,
            });

            console.log('Registration successful', response.data);
            navigate('/auth');

        } catch (error) {
            if (error.response) {
                console.error('Registration failed', error.response.data);
            } else if (error.request) {
                console.error('No response received');
            } else {
                console.error('Error during registration', error.message);
            }
        }

        setUsername('');
        setEmail('');
        setPassword('');
        navigate('/auth');
    };

    return (
        <div className={styles.registrationContainer}>
            <form className={styles.registrationForm} onSubmit={handleSubmit}>
                <h1 className={styles.registrationTitle}>Регистрация в Погоде</h1>
                <input
                    type="text"
                    value={username}
                    onChange={(e) => handleInputChange(e, setUsername)}
                    placeholder="Username"
                    className={styles.inputField}
                />
                <br/>
                <input
                    type="email"
                    value={email}
                    onChange={(e) => handleInputChange(e, setEmail)}
                    placeholder="Почта"
                    className={styles.inputField}
                />
                <br/>
                <input
                    type="password"
                    value={password}
                    onChange={(e) => handleInputChange(e, setPassword)}
                    placeholder="Пароль"
                    className={styles.inputField}
                />
                <br/>

                <button type="submit" className={styles.submitButton}>
                    Зарегистрироваться
                </button>

                <hr className={styles.hrLine}/>

                <label className={styles.labelText}>
                    Есть аккаунт? <span onClick={() => navigate('/auth')} className={styles.linkText}>Войти</span>
                </label>
            </form>
        </div>
    );
}