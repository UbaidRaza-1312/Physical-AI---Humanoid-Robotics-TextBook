
import type {ReactNode} from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import HomepageFeatures from '@site/src/components/HomepageFeatures';
import Heading from '@theme/Heading';

import styles from './index.module.css';

function HomepageHeader() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <header className={clsx('hero hero--primary', styles.heroBanner)}>
      <div className="container">
        <Heading as="h1" className={styles.heroTitle}>
          Empowering the Next Generation of Physical AI
        </Heading>
        <p className={styles.heroSubtitle}>
          Bridging the gap between intelligent algorithms and real-world robotic systems to unlock unprecedented capabilities.
        </p>
        <div className={styles.buttons}>
          <Link
            className="button button--primary button--lg"
            to="/docs/intro">
            Start Your Journey
          </Link>
          <Link
            className="button button--secondary button--lg"
            to="/docs/category/module-1-ros2">
            Explore Modules
          </Link>
        </div>
      </div>
    </header>
  );
}

function AboutSection() {
  return (
    <section className={styles.aboutSection}>
      <div className="container">
        <Heading as="h2">About Physical AI</Heading>
        <p>
          Physical AI represents the convergence of artificial intelligence with robotics, enabling machines to perceive, reason, and act intelligently within dynamic physical environments. Our platform provides comprehensive resources for understanding and developing these cutting-edge systems, from foundational theories to practical applications.
        </p>
      </div>
    </section>
  );
}

export default function Home(): ReactNode {
  const {siteConfig} = useDocusaurusContext();
  return (
    <Layout
      title={`Welcome to ${siteConfig.title}`}
      description="Explore the world of Physical AI and Humanoid Robotics.">
      <HomepageHeader />
      <main>
        <AboutSection /> {/* New About Section */}
        <HomepageFeatures />
      </main>
    </Layout>
  );
}
