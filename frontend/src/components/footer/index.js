import styles from './style.module.css'
import { Container, LinkComponent } from '../index'

// Add a comment here to force a commit and push:
// This line forces Git to see a change.
// This line likely existed but was never committed or so
//const { isFetching, isError, error, isSuccess, isIdle, data, isPaused } = useQuery('...');

const Footer = () => {
  return <footer className={styles.footer}>
      <Container className={styles.footer__container}>
        <LinkComponent href='#' title='Foodgram' className={styles.footer__brand} />
      </Container>
  </footer>
}

export default Footer
