import React from 'react';
import styles from './Header.module.css';


export default function Header({showContactInfo = true}) {
    return (
        <header className={styles.header}>
            <div className={styles.content}>
                {showContactInfo && (
                    <>
                        <div className={styles['contact-info']}>
                            <div className={styles.phone}>
                                8 913 879 03 96
                            </div>
                        </div>
                        <div className={styles['contact-info']}>
                            <div className={styles.email}>
                                tikhonov.igor2028@yandex.ru
                            </div>
                        </div>
                    </>
                )}
            </div>
        </header>
    );
}
