
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

type ModuleItem = {
  title: string;
  Svg: React.ComponentType<React.ComponentProps<'svg'>>;
  description: ReactNode;
  link: string;
};

const ModuleList: ModuleItem[] = [
  {
    title: 'ROS2 Fundamentals',
    Svg: require('@site/static/img/module1.svg').default,
    description: (
      <>
        Dive into the Robot Operating System 2 (ROS2) with core concepts, tools, and best practices for robotic development.
      </>
    ),
    link: '/docs/module1-ros2/ros2-fundamentals',
  },
  {
    title: 'Digital Twin Simulations',
    Svg: require('@site/static/img/module2.svg').default,
    description: (
      <>
        Explore the power of digital twins and simulation environments for testing and validating AI and robotics systems.
      </>
    ),
    link: '/docs/module2-digital-twin/simulation-basics',
  },
  {
    title: 'NVIDIA Isaac Integration',
    Svg: require('@site/static/img/module3.svg').default,
    description: (
      <>
        Learn to integrate NVIDIA Isaac Sim for advanced robotics simulation, perception, and AI model training.
      </>
    ),
    link: '/docs/module3-nvidia-isaac/isaac-perception',
  },
  {
    title: 'VLA Capstone Project',
    Svg: require('@site/static/img/module4.svg').default,
    description: (
      <>
        Apply your knowledge in a comprehensive capstone project, integrating Vision-Language-Action models into a physical system.
      </>
    ),
    link: '/docs/module4-vla-capstone/vla-integration',
  },
];

function Module({title, Svg, description, link}: ModuleItem) {
  return (
    <div className={clsx('col col--3', styles.moduleCard)}> {/* col--3 for 4 modules */}
      <div className="text--center">
        <Svg className={styles.moduleSvg} role="img" />
      </div>
      <div className="text--center padding-horiz--md">
        <Heading as="h3">{title}</Heading>
        <p>{description}</p>
        <Link
            className="button button--primary"
            to={link}>
            Learn More
          </Link>
      </div>
    </div>
  );
}

function ModulesSection() {
  return (
    <section className={styles.modulesSection}>
      <div className="container">
        <Heading as="h2">Explore Our Modules</Heading>
        <div className={clsx('row', styles.modulesGrid)}>
          {ModuleList.map((props, idx) => (
            <Module key={idx} {...props} />
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
        <HomepageFeatures /> {/* Keep features for now, can be moved later if needed */}
        <ModulesSection /> {/* New Modules Section */}
        <AboutSection /> {/* Moved About Section to the end of main */}
      </main>
    </Layout>
  );
}
