import React, {useState, useEffect} from 'react';
import ReactDOM from 'react-dom';
import styles from './Rectangle.module.css';

const Rectangle = () => {
    const [showRectangle, setShowRectangle] = useState(true);

    useEffect(() => {
        const timer = setTimeout(() => {
            setShowRectangle(false);
        }, 4000);

        return () => clearTimeout(timer);
    }, []);

    return ReactDOM.createPortal(
        showRectangle && (
            <div className={styles.rectangle}>
                <div>
                    <p className={styles.text}>Неправильный логин или пароль.</p>
                    <p className={styles.text} type="second">Попробуйте ещё раз.</p>
                </div>
            </div>
        ),
        document.body
    );
};

export default Rectangle;