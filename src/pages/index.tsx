
import type {ReactNode} from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import HomepageFeatures from '@site/src/components/HomepageFeatures';
import Heading from '@theme/Heading';

import ChatWidget from '../components/ChatWidget/index';
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
        </div>
      </div>
    </header>
  );
}

type ModuleItem = {
  title: string;
  description: ReactNode;
  link: string;
};

const ModuleList: ModuleItem[] = [
  {
    title: 'ROS2 Fundamentals',
    description: (
      <>
        Dive into the Robot Operating System 2 (ROS2) with core concepts, tools, and best practices for robotic development.
      </>
    ),
    link: '/docs/module1-ros2/ros2-fundamentals',
  },
  {
    title: 'Digital Twin Simulations',
    description: (
      <>
        Explore the power of digital twins and simulation environments for testing and validating AI and robotics systems.
      </>
    ),
    link: '/docs/module2-digital-twin/simulation-basics',
  },
  {
    title: 'NVIDIA Isaac Integration',
    description: (
      <>
        Learn to integrate NVIDIA Isaac Sim for advanced robotics simulation, perception, and AI model training.
      </>
    ),
    link: '/docs/module3-nvidia-isaac/isaac-perception',
  },
  {
    title: 'VLA Capstone Project',
    description: (
      <>
        Apply your knowledge in a comprehensive capstone project, integrating Vision-Language-Action models into a physical system.
      </>
    ),
    link: '/docs/module4-vla-capstone/vla-integration',
  },
];

function Module({title, description, link, idx}: ModuleItem & {idx: number}) {
  return (
    <div> {/* Responsive columns for modules */}
      <Link to={link} className={clsx(styles.moduleCard, styles.moduleCardLink)}>
        <div className="text--center padding-horiz--md">
          <Heading as="h3">Chapter {idx + 1}: {title}</Heading>
          <p>{description}</p>
        </div>
      </Link>
    </div>
  );
}

function ModulesSection() {
  return (
    <section className={styles.modulesSection}>
      <div className="container">
        <Heading as="h2">Explore Our Modules</Heading>
        <div className={styles.modulesGrid}>
          {ModuleList.map((props, idx) => (
            <Module key={idx} idx={idx} {...props} />
          ))}
        </div>
      </div>
    </section>
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
        <ModulesSection /> {/* New Modules Section */}
        <AboutSection /> {/* Moved About Section to the end of main */}
      </main>
      <ChatWidget />
    </Layout>
  );
}
