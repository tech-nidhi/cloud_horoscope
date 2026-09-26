/**
 * Cloud Horoscope Engine & API Client
 * Provides cosmic AWS cloud-themed horoscopes with full 12 Zodiac sign coverage,
 * support for live AWS API Gateway endpoints, and automatic resilient local fallback.
 */

export const ZODIAC_DATA = {
  Aries: {
    symbol: "♈",
    dates: "Mar 21 - Apr 19",
    element: "Fire",
    luckyService: "AWS Lambda & EC2 Spot",
    luckyRegion: "us-east-1 (N. Virginia)",
    resilienceScore: 98,
    color: "from-red-500 to-orange-500",
    variations: [
      (name) => `Your Lambda functions are charging ahead today, ${name}! Like a true Aries, your EC2 instances will scale with fiery determination. S3 buckets overflow with success, and your CloudWatch metrics show blazing performance. Beware of over-provisioning - even rams need to watch their AWS bill!`,
      (name) => `The cosmic forces ignite your cloud infrastructure today, ${name}! Your Aries energy powers through deployment pipelines like lightning. API Gateway calls flow with unstoppable momentum, while your auto-scaling groups respond to traffic spikes with warrior-like precision. A breakthrough in your CloudFormation templates awaits!`,
      (name) => `Mars aligns with your serverless architecture today, ${name}! Your pioneering Aries spirit leads the charge in container orchestration. ECS tasks launch with military precision, while your load balancers distribute traffic like a strategic battle plan. Victory in your next code deployment is assured!`
    ]
  },
  Taurus: {
    symbol: "♉",
    dates: "Apr 20 - May 20",
    element: "Earth",
    luckyService: "Amazon RDS Multi-AZ & EBS io2",
    luckyRegion: "us-west-2 (Oregon)",
    resilienceScore: 99.99,
    color: "from-emerald-500 to-teal-500",
    variations: [
      (name) => `Steady and reliable like your favorite EBS volumes, ${name}! Your methodical approach to cloud architecture brings stability today. RDS databases respond to your patient queries, while your VPC configurations remain rock-solid. A cost optimization opportunity awaits in your reserved instances.`,
      (name) => `Your Taurus determination builds unshakeable cloud foundations today, ${name}! Like a master architect, your infrastructure design stands the test of time. DynamoDB tables store data with the permanence of ancient monuments, while your backup strategies provide the security of a digital fortress.`,
      (name) => `The earth signs favor your persistent coding efforts today, ${name}! Your Taurus nature ensures every CloudWatch alarm is perfectly tuned. S3 lifecycle policies work with the rhythm of seasons, while your monitoring dashboards reveal patterns with the patience of a seasoned gardener.`
    ]
  },
  Gemini: {
    symbol: "♊",
    dates: "May 21 - Jun 20",
    element: "Air",
    luckyService: "AWS Route 53 & API Gateway",
    luckyRegion: "eu-west-1 (Ireland)",
    resilienceScore: 97,
    color: "from-amber-400 to-yellow-500",
    variations: [
      (name) => `Your dual nature shines in multi-region deployments today, ${name}! Like the twins, your load balancers distribute traffic with perfect harmony. API Gateway calls flow smoothly, and your microservices communicate beautifully. Consider implementing blue-green deployments for extra versatility.`,
      (name) => `Communication flows through your distributed systems today, ${name}! Your Gemini adaptability makes service mesh configurations dance in perfect synchronization. Message queues carry data like whispered secrets between services, while your API documentation sparkles with clarity.`,
      (name) => `The twins bless your dual-stack architecture today, ${name}! Your quick-thinking Gemini mind optimizes both IPv4 and IPv6 configurations simultaneously. Container networking adapts like quicksilver, while your service discovery mechanisms work with telepathic precision.`
    ]
  },
  Cancer: {
    symbol: "♋",
    dates: "Jun 21 - Jul 22",
    element: "Water",
    luckyService: "AWS WAF, Shield & IAM",
    luckyRegion: "ca-central-1 (Central)",
    resilienceScore: 99.9,
    color: "from-cyan-400 to-blue-500",
    variations: [
      (name) => `Your protective instincts serve your security groups well today, ${name}! Like a caring crab, you shield your resources with perfect IAM policies. CloudTrail logs reveal hidden insights, and your backup strategies provide emotional comfort. Trust your intuition about that suspicious network traffic.`,
      (name) => `The moon illuminates your data protection strategies today, ${name}! Your nurturing Cancer nature ensures every database backup is safely nested in multiple availability zones. Encryption keys guard your secrets like a mother protecting her young, while compliance audits pass with flying colors.`,
      (name) => `Your intuitive Cancer wisdom guides disaster recovery planning today, ${name}! Like a protective shell, your security architecture adapts to threats with maternal instinct. WAF rules filter malicious traffic with the care of a guardian, while your incident response procedures flow like tidal rhythms.`
    ]
  },
  Leo: {
    symbol: "♌",
    dates: "Jul 23 - Aug 22",
    element: "Fire",
    luckyService: "AWS Step Functions & CloudFront",
    luckyRegion: "ap-southeast-1 (Singapore)",
    resilienceScore: 99.5,
    color: "from-amber-500 to-rose-500",
    variations: [
      (name) => `Roar with confidence today, ${name}! Your Lambda functions command attention like a true king of the cloud. EC2 instances bow to your scaling prowess, and S3 storage basks in your organizational glory. The stars align for a breakthrough in your CloudFormation templates. Avoid over-provisioning - even lions need to watch their AWS bill!`,
      (name) => `Your Leo magnificence illuminates the entire data center today, ${name}! Like a digital sun king, your architecture radiates performance excellence. CDN distributions carry your content across the globe with royal fanfare, while your monitoring dashboards display metrics worthy of a throne room.`,
      (name) => `The spotlight shines on your serverless mastery today, ${name}! Your Leo leadership transforms complex workflows into elegant Step Functions. Container orchestration follows your commands like a loyal court, while your CI/CD pipelines execute with the precision of a royal decree.`
    ]
  },
  Virgo: {
    symbol: "♍",
    dates: "Aug 23 - Sep 22",
    element: "Earth",
    luckyService: "AWS CloudFormation & Config",
    luckyRegion: "eu-central-1 (Frankfurt)",
    resilienceScore: 100,
    color: "from-emerald-400 to-green-600",
    variations: [
      (name) => `Your attention to detail perfects every CloudFormation template today, ${name}! Like a meticulous Virgo, you optimize every resource with precision. Your monitoring dashboards reveal patterns others miss, and your cost analysis brings order to chaos. A small configuration tweak will yield big performance gains.`,
      (name) => `Perfectionist Virgo energy flows through your code reviews today, ${name}! Every semicolon finds its proper place, while your linting rules maintain pristine standards. Database schemas organize with the precision of a master librarian, and your documentation achieves literary excellence.`,
      (name) => `Your analytical Virgo mind dissects performance metrics today, ${name}! Like a digital surgeon, you identify bottlenecks with microscopic precision. Query optimization becomes an art form, while your capacity planning predicts future needs with prophetic accuracy.`
    ]
  },
  Libra: {
    symbol: "♎",
    dates: "Sep 23 - Oct 22",
    element: "Air",
    luckyService: "AWS Application Load Balancer & Auto Scaling",
    luckyRegion: "us-east-2 (Ohio)",
    resilienceScore: 98.8,
    color: "from-pink-400 to-indigo-500",
    variations: [
      (name) => `Balance flows through your architecture today, ${name}! Your load balancers achieve perfect harmony, while auto-scaling groups maintain ideal equilibrium. API rate limits find their sweet spot, and your multi-AZ deployments create beautiful symmetry. Seek consensus before that major infrastructure change.`,
      (name) => `Harmony resonates through your distributed systems today, ${name}! Your Libra sense of justice ensures fair resource allocation across all services. Traffic routing achieves perfect balance, while your service mesh creates elegant patterns of interconnection that would make artists weep with joy.`,
      (name) => `The scales of cloud architecture tip in your favor today, ${name}! Your diplomatic Libra nature negotiates perfect SLAs between competing services. Consensus algorithms reach agreement with the grace of a peace treaty, while your conflict resolution in merge requests becomes legendary.`
    ]
  },
  Scorpio: {
    symbol: "♏",
    dates: "Oct 23 - Nov 21",
    element: "Water",
    luckyService: "AWS Secrets Manager & GuardDuty",
    luckyRegion: "ap-northeast-1 (Tokyo)",
    resilienceScore: 99.7,
    color: "from-purple-600 to-pink-600",
    variations: [
      (name) => `Your penetrating insights uncover hidden security vulnerabilities today, ${name}! Like a determined Scorpio, you dive deep into CloudTrail logs and emerge with powerful revelations. Your encryption strategies intensify, and database connections transform mysteriously. Trust your instincts about that anomalous traffic pattern.`,
      (name) => `The depths of your data lake reveal their secrets today, ${name}! Your Scorpio intensity transforms raw logs into actionable intelligence. Like a digital detective, you trace performance issues to their source, while your forensic analysis of system behavior borders on the supernatural.`,
      (name) => `Your Scorpio passion ignites breakthrough innovations today, ${name}! Deep learning models respond to your intense focus, while your data mining operations unearth hidden patterns like precious gems. Security penetration testing reveals vulnerabilities that lesser minds would miss entirely.`
    ]
  },
  Sagittarius: {
    symbol: "♐",
    dates: "Nov 22 - Dec 21",
    element: "Fire",
    luckyService: "Amazon CloudFront Edge & Global Accelerator",
    luckyRegion: "sa-east-1 (São Paulo)",
    resilienceScore: 96.5,
    color: "from-violet-500 to-fuchsia-600",
    variations: [
      (name) => `Adventure calls from distant AWS regions today, ${name}! Your global deployments expand horizons like a true Sagittarius archer. CloudFront distributions carry your content to far-off lands, while your wandering spirit discovers new services. Aim high with that ambitious migration project!`,
      (name) => `Your Sagittarius wanderlust explores uncharted cloud territories today, ${name}! Like a digital nomad, you discover optimal regions for workload placement. Edge locations become waypoints on your global journey, while your architectural vision spans continents with the scope of an explorer's map.`,
      (name) => `The archer's arrow finds its target in perfect deployments today, ${name}! Your Sagittarius optimism tackles the most ambitious cloud migrations with infectious enthusiasm. Multi-cloud strategies unfold like epic journeys, while your knowledge sharing inspires teams across time zones.`
    ]
  },
  Capricorn: {
    symbol: "♑",
    dates: "Dec 22 - Jan 19",
    element: "Earth",
    luckyService: "AWS Organizations, SCPs & Well-Architected Tool",
    luckyRegion: "us-west-1 (N. California)",
    resilienceScore: 99.999,
    color: "from-slate-600 to-zinc-800",
    variations: [
      (name) => `Your methodical approach to cloud architecture reaches new heights today, ${name}! Like a mountain goat scaling AWS peaks, your systematic deployment strategies will reach new summits. RDS databases respond to your structured queries, while VPC configurations align perfectly. The stars suggest a cost optimization opportunity in your unused Elastic IPs.`,
      (name) => `Your Capricorn discipline builds enterprise-grade solutions today, ${name}! Like a master craftsman, every component fits with architectural precision. Governance policies enforce standards with the authority of natural law, while your long-term capacity planning ensures sustainable growth for decades.`,
      (name) => `The mountain peak of cloud mastery comes into view today, ${name}! Your persistent Capricorn nature transforms complex requirements into elegant solutions. Compliance frameworks align like geological strata, while your systematic approach to technical debt creates lasting value.`
    ]
  },
  Aquarius: {
    symbol: "♒",
    dates: "Jan 20 - Feb 18",
    element: "Air",
    luckyService: "Amazon Bedrock AI & Amazon Braket",
    luckyRegion: "ap-south-1 (Mumbai)",
    resilienceScore: 98.5,
    color: "from-teal-400 to-cyan-600",
    variations: [
      (name) => `Innovation flows through your serverless functions today, ${name}! Your revolutionary ideas transform traditional architectures, while your humanitarian spirit optimizes costs for everyone. Step Functions orchestrate workflows with Aquarian precision. That experimental service you've been eyeing? Today's the day to try it!`,
      (name) => `Your Aquarius vision revolutionizes cloud paradigms today, ${name}! Like a digital prophet, you see possibilities others cannot imagine. Quantum computing services respond to your forward-thinking approach, while your open-source contributions benefit the entire community with altruistic generosity.`,
      (name) => `The water bearer pours innovation into your infrastructure today, ${name}! Your Aquarius independence breaks free from conventional patterns, creating architectures that defy traditional boundaries. Edge computing networks form constellations of possibility under your visionary guidance.`
    ]
  },
  Pisces: {
    symbol: "♓",
    dates: "Feb 19 - Mar 20",
    element: "Water",
    luckyService: "Amazon Kinesis & DynamoDB Streams",
    luckyRegion: "eu-north-1 (Stockholm)",
    resilienceScore: 97.9,
    color: "from-blue-400 to-indigo-600",
    variations: [
      (name) => `Your Lambda functions are swimming in success today, ${name}! The cosmic EC2 currents favor your deployments, while S3 buckets overflow with data treasures. CloudWatch metrics show positive energy flowing through your infrastructure. A mysterious DynamoDB query may reveal hidden insights this afternoon.`,
      (name) => `Your intuitive Pisces nature navigates data streams today, ${name}! Like a digital mystic, you sense patterns in chaos and find meaning in metrics. Machine learning models respond to your empathetic approach, while your user experience designs create emotional connections that transcend mere functionality.`,
      (name) => `The fish swim in perfect formation through your data pipelines today, ${name}! Your Pisces creativity transforms mundane ETL processes into works of art. Stream processing flows with the rhythm of ocean currents, while your compassionate approach to error handling creates graceful degradation patterns.`
    ]
  }
};

const ZODIAC_DATE_RANGES = [
  { start: [3, 21], end: [4, 19], sign: "Aries" },
  { start: [4, 20], end: [5, 20], sign: "Taurus" },
  { start: [5, 21], end: [6, 20], sign: "Gemini" },
  { start: [6, 21], end: [7, 22], sign: "Cancer" },
  { start: [7, 23], end: [8, 22], sign: "Leo" },
  { start: [8, 23], end: [9, 22], sign: "Virgo" },
  { start: [9, 23], end: [10, 22], sign: "Libra" },
  { start: [10, 23], end: [11, 21], sign: "Scorpio" },
  { start: [11, 22], end: [12, 21], sign: "Sagittarius" },
  { start: [12, 22], end: [1, 19], sign: "Capricorn" },
  { start: [1, 20], end: [2, 18], sign: "Aquarius" },
  { start: [2, 19], end: [3, 20], sign: "Pisces" }
];

/**
 * Determine zodiac sign from day and month
 */
export function getZodiacSign(day, month) {
  for (const range of ZODIAC_DATE_RANGES) {
    const [startMonth, startDay] = range.start;
    const [endMonth, endDay] = range.end;

    if (startMonth <= endMonth) {
      if (
        (month === startMonth && day >= startDay) ||
        (month === endMonth && day <= endDay) ||
        (month > startMonth && month < endMonth)
      ) {
        return range.sign;
      }
    } else {
      // Capricorn spans year boundary (Dec 22 to Jan 19)
      if (
        (month === startMonth && day >= startDay) ||
        (month === endMonth && day <= endDay)
      ) {
        return range.sign;
      }
    }
  }
  return "Aries";
}

/**
 * Parse date string safely without UTC/timezone drift
 */
export function parseDob(dobString) {
  if (!dobString) return null;
  // Support YYYY-MM-DD or DD/MM/YYYY or DD-MM-YYYY
  if (dobString.includes('-')) {
    const parts = dobString.split('-');
    if (parts[0].length === 4) {
      // YYYY-MM-DD
      const year = parseInt(parts[0], 10);
      const month = parseInt(parts[1], 10);
      const day = parseInt(parts[2], 10);
      return { day, month, year, formatted: `${String(day).padStart(2, '0')}/${String(month).padStart(2, '0')}/${year}` };
    } else {
      // DD-MM-YYYY
      const day = parseInt(parts[0], 10);
      const month = parseInt(parts[1], 10);
      const year = parseInt(parts[2], 10);
      return { day, month, year, formatted: `${String(day).padStart(2, '0')}/${String(month).padStart(2, '0')}/${year}` };
    }
  } else if (dobString.includes('/')) {
    const parts = dobString.split('/');
    const day = parseInt(parts[0], 10);
    const month = parseInt(parts[1], 10);
    const year = parseInt(parts[2], 10);
    return { day, month, year, formatted: dobString };
  }
  return null;
}

/**
 * Generate local cosmic horoscope
 */
export function generateLocalHoroscope(name, dobString, variationOffset = 0) {
  const parsed = parseDob(dobString);
  if (!parsed || isNaN(parsed.day) || isNaN(parsed.month)) {
    throw new Error("Invalid date of birth provided.");
  }

  const sign = getZodiacSign(parsed.day, parsed.month);
  const signInfo = ZODIAC_DATA[sign] || ZODIAC_DATA.Aries;

  const variations = signInfo.variations;
  const index = Math.abs((name.length + variationOffset) % variations.length);
  const horoscopeText = variations[index](name.trim());

  return {
    project: "Cloud Horoscope",
    author: "AWS Bedrock Cosmic Engine",
    sign: sign,
    symbol: signInfo.symbol,
    dates: signInfo.dates,
    element: signInfo.element,
    luckyService: signInfo.luckyService,
    luckyRegion: signInfo.luckyRegion,
    resilienceScore: signInfo.resilienceScore,
    color: signInfo.color,
    horoscope: horoscopeText,
    source: "local-engine",
    timestamp: new Date().toISOString()
  };
}

/**
 * Fetch horoscope from custom or default API, with seamless local fallback
 */
export async function getHoroscope({ name, dob, apiEndpoint = null, variationOffset = 0 }) {
  const parsed = parseDob(dob);
  if (!parsed) {
    throw new Error("Please enter a valid date of birth.");
  }

  // Live AWS API Gateway deployed endpoint
  const DEFAULT_AWS_ENDPOINT = 'https://cryq8fxp5k.execute-api.us-east-1.amazonaws.com';
  const targetEndpoint = apiEndpoint || localStorage.getItem('custom_horoscope_api_endpoint') || DEFAULT_AWS_ENDPOINT;

  // If a remote endpoint is configured, attempt fetch
  if (targetEndpoint && targetEndpoint.trim()) {
    try {
      const response = await fetch(targetEndpoint.trim(), {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          name: name.trim(),
          dob: parsed.formatted
        })
      });

      if (response.ok) {
        const data = await response.json();
        const sign = data.sign || getZodiacSign(parsed.day, parsed.month);
        const signInfo = ZODIAC_DATA[sign] || ZODIAC_DATA.Aries;
        return {
          project: data.project || "Cloud Horoscope",
          author: data.author || "AWS Lambda Function",
          sign: sign,
          symbol: signInfo.symbol,
          dates: signInfo.dates,
          element: signInfo.element,
          luckyService: signInfo.luckyService,
          luckyRegion: signInfo.luckyRegion,
          resilienceScore: signInfo.resilienceScore,
          color: signInfo.color,
          horoscope: data.horoscope,
          source: "aws-api",
          timestamp: new Date().toISOString()
        };
      } else {
        console.warn("Remote API responded with error status, falling back to local cosmic engine.");
      }
    } catch (networkError) {
      console.warn("Could not connect to remote API Gateway, using local cosmic engine fallback:", networkError.message);
    }
  }

  // Graceful, guaranteed working local cosmic engine
  // Simulate natural cosmic calculation time for engaging UI feel
  await new Promise((res) => setTimeout(res, 600));
  return generateLocalHoroscope(name, dob, variationOffset);
}
