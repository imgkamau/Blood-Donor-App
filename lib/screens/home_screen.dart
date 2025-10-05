import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:url_launcher/url_launcher.dart';
import '../themes/app_theme.dart';
import '../providers/app_provider.dart';
import 'donor/enrollment_screen.dart';
import 'recipient/search_screen.dart';
import 'legal/terms_conditions_screen.dart';
import '../widgets/common/gradient_button.dart';
import '../widgets/common/feature_card.dart';

class HomeScreen extends StatelessWidget {
  const HomeScreen({super.key});

  static Future<void> _launchWebsite(BuildContext context) async {
    const url = 'https://blood-donor-app.vercel.app/';
    try {
      final uri = Uri.parse(url);
      if (await canLaunchUrl(uri)) {
        await launchUrl(uri, mode: LaunchMode.externalApplication);
      } else {
        _showErrorSnackBar(context, 'Could not open website');
      }
    } catch (e) {
      _showErrorSnackBar(context, 'Error opening website: $e');
    }
  }

  static void _showErrorSnackBar(BuildContext context, String message) {
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Text(message),
        backgroundColor: AppTheme.error,
        behavior: SnackBarBehavior.floating,
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(8),
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Container(
        decoration: AppTheme.redGradientDecoration,
        child: SafeArea(
          child: Column(
            children: [
              // Header Section
              Padding(
                padding: const EdgeInsets.all(24.0),
                child: Column(
                  children: [
                    // App Logo/Icon
                    Container(
                      width: 80,
                      height: 80,
                      decoration: BoxDecoration(
                        color: Colors.white.withOpacity(0.2),
                        borderRadius: BorderRadius.circular(20),
                      ),
                      child: const Icon(
                        Icons.favorite,
                        color: Colors.white,
                        size: 40,
                      ),
                    ),
                    const SizedBox(height: 16),
                    
                    // Subtitle
                    Text(
                      'Connecting lives, saving lives',
                      style: Theme.of(context).textTheme.titleLarge?.copyWith(
                        color: Colors.white,
                        fontWeight: FontWeight.w600,
                      ),
                    ),
                  ],
                ),
              ),
              
              // Main Content
              Expanded(
                child: Container(
                  decoration: const BoxDecoration(
                    color: Colors.white,
                    borderRadius: BorderRadius.only(
                      topLeft: Radius.circular(30),
                      topRight: Radius.circular(30),
                    ),
                  ),
                  child: Padding(
                    padding: const EdgeInsets.all(24.0),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        // Welcome Text
                        Text(
                          'Welcome!',
                          style: Theme.of(context).textTheme.headlineLarge?.copyWith(
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                        const SizedBox(height: 8),
                        Text(
                          'Choose how you\'d like to help or get help',
                          style: Theme.of(context).textTheme.bodyLarge?.copyWith(
                            color: AppTheme.grey,
                          ),
                        ),
                        const SizedBox(height: 32),
                        
                        // Main Action Buttons
                        GradientButton(
                          text: 'I Want to Donate Blood',
                          icon: Icons.favorite,
                          onPressed: () {
                            Navigator.push(
                              context,
                              MaterialPageRoute(
                                builder: (context) => const EnrollmentScreen(),
                              ),
                            );
                          },
                        ),
                        const SizedBox(height: 16),
                        
                        GradientButton(
                          text: 'I Need Blood',
                          icon: Icons.search,
                          onPressed: () {
                            Navigator.push(
                              context,
                              MaterialPageRoute(
                                builder: (context) => const SearchScreen(),
                              ),
                            );
                          },
                          isSecondary: true,
                        ),
                        const SizedBox(height: 32),
                        
                        // Features Section
                        Text(
                          'How it works',
                          style: Theme.of(context).textTheme.headlineMedium?.copyWith(
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                        const SizedBox(height: 16),
                        
                        // Feature Cards
                        Expanded(
                          child: ListView(
                            children: const [
                              FeatureCard(
                                icon: Icons.person_add,
                                title: 'Register as Donor',
                                description: 'Sign up with your blood type and location to help save lives',
                              ),
                              SizedBox(height: 12),
                              FeatureCard(
                                icon: Icons.location_on,
                                title: 'Find Nearby Donors',
                                description: 'Get contacts of compatible donors within 50km radius',
                              ),
                              SizedBox(height: 12),
                              FeatureCard(
                                icon: Icons.phone,
                                title: 'Contact & Save Lives',
                                description: 'Reach out to donors and help save precious lives',
                              ),
                            ],
                          ),
                        ),
                        
                        // Links Section
                        const SizedBox(height: 16),
                        Row(
                          mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                          children: [
                            TextButton(
                              onPressed: () {
                                Navigator.push(
                                  context,
                                  MaterialPageRoute(
                                    builder: (context) => const TermsConditionsScreen(),
                                  ),
                                );
                              },
                              child: Text(
                                'Terms & Conditions',
                                style: Theme.of(context).textTheme.bodySmall?.copyWith(
                                  color: AppTheme.grey,
                                  decoration: TextDecoration.underline,
                                ),
                              ),
                            ),
                            TextButton(
                              onPressed: () {
                                _launchWebsite(context);
                              },
                              child: Text(
                                'Visit Website',
                                style: Theme.of(context).textTheme.bodySmall?.copyWith(
                                  color: AppTheme.primaryRed,
                                  decoration: TextDecoration.underline,
                                  fontWeight: FontWeight.w500,
                                ),
                              ),
                            ),
                          ],
                        ),
                      ],
                    ),
                  ),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}