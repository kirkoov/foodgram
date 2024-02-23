import { Title, Pagination, Container, Main, SubscriptionList  } from '../../components'
import { useSubscriptions } from '../../utils'
import api from '../../api'
import { useEffect } from 'react'
import MetaTags from 'react-meta-tags'

const SubscriptionsPage = () => {
  const {
    subscriptions,
    setSubscriptions,
    subscriptionsCount,
    setSubscriptionsCount,
    removeSubscription,
    subscriptionsPage,
    setSubscriptionsPage
  } = useSubscriptions()

  const getSubscriptions = ({ page }) => {
    api
      .getSubscriptions({ page })
      .then(res => {
        setSubscriptions(res.results)
        setSubscriptionsCount(res.count)
      })
  }

  useEffect(_ => {
    getSubscriptions({ page: subscriptionsPage })
  }, [subscriptionsPage])


  return <Main>
    <Container>
      <MetaTags>
        <title>My subscriptions</title>
        <meta name="description" content="Foodgram - My subscriptions" />
        <meta property="og:title" content="My subscriptions" />
      </MetaTags>
      <Title
        title='My subscriptions'
      />
      <SubscriptionList
        subscriptions={subscriptions}
        removeSubscription={removeSubscription}
      />
      <Pagination
        count={subscriptionsCount}
        limit={6}
        onPageChange={page => {
          setSubscriptionsPage(page)
        }}
      />
    </Container>
  </Main>
}

export default SubscriptionsPage
