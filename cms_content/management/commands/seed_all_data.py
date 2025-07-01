import os
from django.core.management.base import BaseCommand
from django.conf import settings
from django.core.files import File
from cms_content.models import Product, ProductImage, ProductSection, ProductSectionItem, Service

class Command(BaseCommand):
    help = 'Seeds the database with all product data and images.'

    def handle(self, *args, **options):
        self.stdout.write('Starting database seeding...')

        products_data = [
            {
                "name": "Robodogs",
                "short_description": "AI-powered quadrupeds for inspection, surveillance, and operational efficiency.",
                "hero_image": "static/images/products/robodog.png",
                "main_description": "Our AI-powered Robodogs are designed for high-mobility, adaptability, and intelligence, transforming inspection, surveillance, and operational efficiency in challenging environments like industrial sites, hazardous areas, and remote locations.",
                "conclusion_text": "Our Robodogs redefine efficiency, safety, and automation across industries, positioning Leafloat Robotics at the forefront of intelligent robotic solutions.",
                "url_slug": "robodogs",
                "order": 1,
                "images": [
                    "static/images/products/1.png",
                ],
                "sections": [
                    {
                        "title": "Key Features",
                        "items": [
                            "AI-Driven Autonomy & Navigation: Advanced SLAM, obstacle detection, and GPS/RTK-enabled localization for precise navigation.",
                            "High-Mobility Quadrupedal Design: Agile movement across rough terrains, stairs, and obstacles with adaptive walking modes.",
                            "Advanced Sensor Suite: 360° LiDAR, thermal/RGB cameras, and gas/chemical sensors for real-time environment analysis.",
                            "Autonomous Inspection: AI-powered defect detection, automated data logging, and live-streaming capabilities.",
                            "Remote Operation & Cloud Connectivity: Remote control, cloud-based data storage, and integration with industrial IoT systems."
                        ]
                    },
                    {
                        "title": "Applications",
                        "items": [
                            "Industrial Inspection: Structural assessments, pipeline monitoring, and anomaly detection in machinery.",
                            "Hazardous Environment Monitoring: Radiation/gas leak detection and safety checks in high-risk areas.",
                            "Security & Surveillance: AI-based threat detection and patrolling in restricted zones.",
                            "Search & Rescue: Survivor detection and real-time mapping in disaster zones."
                        ]
                    }
                ]
            },
            {
                "name": "Unmanned Aerial Vehicles (UAVs)",
                "short_description": "Precision agriculture drones for data collection, farm management, and crop yield optimization.",
                "hero_image": "static/images/products/uavs.png",
                "main_description": "Leafloat Robotics’ UAVs are tailored for precision agriculture, optimizing data collection, farm management, and crop yield through AI, multispectral imaging, and autonomous flight capabilities.",
                "conclusion_text": "Our UAV solutions empower farmers with cutting-edge technology to boost productivity, reduce costs, and achieve sustainable agriculture.",
                "url_slug": "uavs",
                "order": 2,
                "images": [
                    "static/images/products/2.png",
                ],
                "sections": [
                    {
                        "title": "Key Features",
                        "items": [
                            "High-Resolution Imaging: RGB, multispectral, and thermal cameras for crop analysis, plus LiDAR for terrain mapping.",
                            "AI-Powered Data Analysis: Real-time crop health monitoring, disease detection, and yield prediction.",
                            "Autonomous Flight & Navigation: Pre-programmed flight paths, GPS/RTK positioning, and collision avoidance.",
                            "Cloud-Based Data Management: Secure storage and integration with farm management software.",
                            "Customizable Payloads: Modular design with pesticide sprayers, NDVI sensors, and hyperspectral cameras."
                        ]
                    }
                ]
            },
            {
                "name": "Unmanned Ground Vehicles (UGVs)",
                "short_description": "Multi-purpose autonomous vehicles for agriculture, construction, and warehouse automation.",
                "hero_image": "static/images/products/3.png",
                "main_description": "Leafloat Robotics’ UGVs are designed for multi-purpose applications in agriculture, construction, and warehouse automation, integrating AI-driven autonomy, robust sensors, and adaptable payloads.",
                "conclusion_text": "Our UGVs deliver seamless automation, enhancing efficiency and productivity across agriculture, construction, and warehouses.",
                "url_slug": "ugvs",
                "order": 3,
                "images": [],
                "sections": [
                    {
                        "title": "Applications",
                        "items": [
                            "Agriculture: Precision planting, weed control, and soil monitoring.",
                            "Construction: Material transport, site surveying, and automated machinery support.",
                            "Warehouses: Goods transportation, inventory scanning, and labor reduction."
                        ]
                    }
                ]
            },
            {
                "name": "Non-GPS Navigation",
                "short_description": "Enabling autonomous operation in GPS-denied environments.",
                "hero_image": "static/images/products/4.png",
                "main_description": "Leafloat Robotics’ non-GPS navigation solutions enable drones and ground vehicles to operate in GPS-denied environments like forests, tunnels, and urban areas using RTK positioning, visual sensors, and AI-driven sensor fusion.",
                "conclusion_text": "Our non-GPS navigation solutions redefine autonomous mobility in GPS-restricted environments, ensuring reliable operation in complex terrains.",
                "url_slug": "non-gps-navigation",
                "order": 4,
                "images": [],
                "sections": [
                    {
                        "title": "Key Technologies",
                        "items": [
                            "RTK-Based Positioning: Centimeter-level accuracy using ground-based stations.",
                            "Visual Odometry & SLAM: AI-powered visual processing for real-time navigation and mapping.",
                            "LiDAR & Depth Sensing: 3D environment perception and obstacle avoidance.",
                            "Inertial Navigation System (INS): Combines IMU with RTK and visual odometry for stability.",
                            "AI-Powered Decision Making: Adaptive navigation and error correction in unknown environments."
                        ]
                    }
                ]
            },
            {
                "name": "Nature Digitization",
                "short_description": "AI-powered tree and fruit classification for precision agriculture.",
                "hero_image": "static/images/products/5.png",
                "main_description": "Leafloat Robotics is revolutionizing precision agriculture with AI-powered solutions for fruit tree detection, classification, and yield estimation, integrating deep learning, computer vision, and 3D mapping for smarter orchard management.",
                "conclusion_text": "Our AI-driven solutions digitize nature, empowering farmers with precise insights for optimized yield, sustainability, and food security.",
                "url_slug": "nature-digitization",
                "order": 5,
                "images": [],
                "sections": [
                    {
                        "title": "Key Features",
                        "items": [
                            "Tree & Fruit Detection/Classification: Deep learning for real-time identification of tree species, growth stages, fruit types, ripeness, and quality, with high accuracy in dense environments.",
                            "3D Mapping & Digital Twins: LiDAR and photogrammetry for orchard modeling and canopy analysis.",
                            "Yield Estimation & Growth Monitoring: AI-driven fruit counting and harvest prediction.",
                            "Health Monitoring: Multispectral/hyperspectral imaging for early disease, pest, and nutrient deficiency detection.",
                            "Autonomous Data Collection: UAVs/UGVs for automated scanning and cloud-based analytics.",
                            "Conveyor-Based Sorting: High-speed AI classification for defect detection and quality control."
                        ]
                    }
                ]
            },
            {
                "name": "Crowd Monitoring",
                "short_description": "AI-powered crowd monitoring for safety and space optimization.",
                "hero_image": "static/images/products/6.png",
                "main_description": "Leafloat Robotics’ AI-powered crowd monitoring system uses computer vision and real-time analytics to manage crowd density in high-traffic areas like malls, event halls, and airports, ensuring safety and optimizing space utilization.",
                "conclusion_text": "Our crowd monitoring system revolutionizes foot traffic management, ensuring safety and efficiency with real-time analytics.",
                "url_slug": "crowd-monitoring",
                "order": 6,
                "images": [],
                "sections": [
                    {
                        "title": "Key Features",
                        "items": [
                            "Real-Time Crowd Density Analysis: AI-driven video processing and heatmap visualization.",
                            "Capacity Monitoring & Compliance: Automated alerts for overcrowding and regulatory compliance.",
                            "Behavioral Analytics: Tracks movement patterns and predicts congestion points.",
                            "Security & Anomaly Detection: Identifies unusual behavior or security threats.",
                            "Data-Driven Insights: Dashboard visualization and forecasting for peak traffic."
                        ]
                    }
                ]
            }
        ]

        for product_data in products_data:
            product, created = Product.objects.update_or_create(
                name=product_data['name'],
                defaults={
                    'short_description': product_data['short_description'],
                    'main_description': product_data['main_description'],
                    'conclusion_text': product_data['conclusion_text'],
                    'url_slug': product_data['url_slug'],
                    'order': product_data['order'],
                    'hero_image_alt_text': product_data['name']
                }
            )

            if created:
                self.stdout.write(self.style.SUCCESS(f'Successfully created product: {product.name}'))
            else:
                self.stdout.write(self.style.WARNING(f'Product already exists, updated: {product.name}'))

            # Handle hero image
            hero_image_path = os.path.join(settings.BASE_DIR, product_data['hero_image'])
            if os.path.exists(hero_image_path):
                with open(hero_image_path, 'rb') as f:
                    product.hero_image.save(os.path.basename(hero_image_path), File(f), save=True)

            # Handle additional images
            for image_path in product_data.get('images', []):
                full_image_path = os.path.join(settings.BASE_DIR, image_path)
                if os.path.exists(full_image_path):
                    image_instance, img_created = ProductImage.objects.get_or_create(
                        product=product,
                        alt_text=f"{product.name} image"
                    )
                    with open(full_image_path, 'rb') as f:
                        image_instance.image.save(os.path.basename(full_image_path), File(f), save=True)

            # Handle sections and items
            for section_data in product_data.get('sections', []):
                section, sec_created = ProductSection.objects.get_or_create(
                    product=product,
                    title=section_data['title']
                )
                for item_text in section_data.get('items', []):
                    ProductSectionItem.objects.get_or_create(
                        section=section,
                        text=item_text
                    )

        self.stdout.write(self.style.SUCCESS('Database seeding complete.'))

        self.stdout.write('Seeding services...')
        services_data = [
            {
                "name": "Robotics Services",
                "short_description": "Comprehensive robotics solutions including UGVs, UAVs, Robodogs, and more.",
                "image": "static/images/services/robotics.jpg",
                "url_slug": "robotics-services",
                "order": 1
            },
            {
                "name": "AI Services",
                "short_description": "Advanced AI solutions for various industries, from warehouse management to safety AI software.",
                "image": "static/images/services/ai.jpg",
                "url_slug": "ai-services",
                "order": 2
            },
            {
                "name": "Rentals",
                "short_description": "Flexible rental options for our state-of-the-art drones and Robodogs.",
                "image": "static/images/services/rentals.jpg",
                "url_slug": "rentals",
                "order": 3
            }
        ]

        for service_data in services_data:
            service, created = Service.objects.update_or_create(
                name=service_data['name'],
                defaults={
                    'short_description': service_data['short_description'],
                    'url_slug': service_data['url_slug'],
                    'order': service_data['order'],
                    'image_alt_text': service_data['name']
                }
            )

            if created:
                self.stdout.write(self.style.SUCCESS(f'Successfully created service: {service.name}'))
            else:
                self.stdout.write(self.style.WARNING(f'Service already exists, updated: {service.name}'))

            # Handle service image
            image_path = os.path.join(settings.BASE_DIR, service_data['image'])
            if os.path.exists(image_path):
                with open(image_path, 'rb') as f:
                    service.image.save(os.path.basename(image_path), File(f), save=True)
        self.stdout.write(self.style.SUCCESS('Service seeding complete.'))
