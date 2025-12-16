import styles from './style.module.css'
import { Container, LinkComponent } from '../index'

// This trivial change forces the clean state of this file to be committed to the remote.

const Footer = () => {
  return <footer className={styles.footer}>
      <Container className={styles.footer__container}>
        <LinkComponent href='#' title='Foodgram' className={styles.footer__brand} />
      </Container>
  </footer>
}

export default Footer
