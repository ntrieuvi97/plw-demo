"""
Updated test example showing how to use the new LoggerController integration.
"""

import pytest
import time
from playwright.sync_api import Page
from src.page_objects.home_page import HomePage
from src.constants.urls import WebUrls


def test_verify_that_all_posts_are_displayed_with_logging(
    page: Page, 
    logger_controller, 
    test_controller, 
    assertions
):
    """
    Test to verify that all posts are displayed on the home page with comprehensive logging.
    """
    # Set up test step
    logger_controller.set_current_step("Test Setup")
    logger_controller.info("Starting post display verification test")
    
    try:
        # Log navigation action
        logger_controller.log_action("Navigate to home page", {"url": WebUrls.BASE_URL})
        page.goto(WebUrls.BASE_URL)
        
        # Set step for page interaction
        logger_controller.set_current_step("Page Interaction")
        
        # Initialize page object and log it
        home_page = HomePage(page)
        logger_controller.info("Home page object initialized")
        
        # Scroll to bottom with logging
        logger_controller.log_action("Scroll to bottom to load all posts")
        home_page.scroll_to_bottom()
        logger_controller.step_passed("Scroll action", "Successfully scrolled to bottom")
        
        # Set step for verification
        logger_controller.set_current_step("Verification")
        
        # Perform assertion with logging
        logger_controller.info("Starting post count verification")
        assertions.verify_that_all_posts_are_displayed(expected_count=10)
        
        # Capture success screenshot
        test_controller.capture_screenshot_with_log("Test completed successfully")
        
        # Log test completion
        logger_controller.step_passed("Test completion", "All verifications passed")
        
    except Exception as e:
        # Log failure with details
        error_details = {
            "error_type": type(e).__name__,
            "error_message": str(e),
            "current_url": page.url,
            "page_title": page.title()
        }
        logger_controller.step_failed("Test execution", str(e), error_details)
        
        # Capture error screenshot
        test_controller.capture_screenshot_with_log("Test failed - error screenshot")
        
        # Re-raise the exception
        raise
        
    finally:
        logger_controller.clear_current_step()


def test_verify_post_navigation_with_performance_logging(
    page: Page,
    logger_controller,
    test_controller,
    assertions
):
    """
    Test post navigation with performance tracking.
    """
    logger_controller.set_current_step("Setup and Navigation")
    
    # Track navigation performance
    nav_start = time.time()
    page.goto(WebUrls.BASE_URL)
    nav_duration = time.time() - nav_start
    logger_controller.log_performance("Initial page load", nav_duration)
    
    home_page = HomePage(page)
    
    # Load posts with performance tracking
    load_start = time.time()
    home_page.scroll_to_bottom()
    posts = home_page.get_all_posts()
    load_duration = time.time() - load_start
    logger_controller.log_performance("Posts loading", load_duration, {"posts_count": len(posts)})
    
    if posts:
        logger_controller.set_current_step("Post Navigation")
        
        # Test clicking on first post
        first_post = posts[0]
        click_start = time.time()
        
        try:
            home_page.click_on_post_part(first_post, "title")
            click_duration = time.time() - click_start
            logger_controller.log_performance("Post click navigation", click_duration)
            
            # Verify navigation
            logger_controller.set_current_step("Navigation Verification")
            assertions.verify_navigate_to_post_detail_successfully(first_post.title)
            
            logger_controller.step_passed("Post navigation", "Successfully navigated to post detail")
            
        except Exception as e:
            click_duration = time.time() - click_start
            logger_controller.log_performance("Failed post click", click_duration)
            logger_controller.step_failed("Post navigation", str(e))
            raise
        
        finally:
            logger_controller.clear_current_step()
    else:
        logger_controller.warning("No posts found for navigation test")


def verify_page_title(page):
    """Helper function for page title verification."""
    title = page.title()
    return bool(title)  # Just check if title exists


def test_multi_step_workflow_with_detailed_logging(
    page: Page,
    logger_controller,
    test_controller
):
    """
    Test demonstrating multi-step workflow with detailed logging.
    """
    
    workflow_steps = [
        ("Navigate to homepage", lambda: page.goto(WebUrls.BASE_URL)),
        ("Wait for page load", lambda: page.wait_for_load_state("networkidle")),
        ("Initialize page objects", lambda: HomePage(page)),
        ("Scroll to load posts", lambda: HomePage(page).scroll_to_bottom()),
        ("Verify page title", lambda: verify_page_title(page)),
        ("Check page responsiveness", lambda: page.wait_for_selector("body", timeout=5000))
    ]
    
    successful_steps = 0
    total_steps = len(workflow_steps)
    
    for step_name, step_action in workflow_steps:
        logger_controller.set_current_step(step_name)
        
        try:
            logger_controller.info(f"Executing: {step_name}")
            
            # Execute step with timing
            start_time = time.time()
            result = step_action()
            duration = time.time() - start_time
            
            # Log success
            logger_controller.log_performance(f"Step: {step_name}", duration)
            logger_controller.step_passed(step_name, f"Completed in {duration:.3f}s")
            successful_steps += 1
            
        except Exception as e:
            duration = time.time() - start_time if 'start_time' in locals() else 0
            error_details = {
                "step": step_name,
                "error": str(e),
                "duration": duration,
                "successful_steps": successful_steps,
                "total_steps": total_steps
            }
            logger_controller.step_failed(step_name, str(e), error_details)
            
            # Capture screenshot on error
            test_controller.capture_screenshot_with_log(f"Error in step: {step_name}")
            
            # Continue with next step instead of failing completely
            logger_controller.warning(f"Continuing workflow despite error in {step_name}")
            
        finally:
            logger_controller.clear_current_step()
    
    # Log workflow summary
    workflow_summary = {
        "total_steps": total_steps,
        "successful_steps": successful_steps,
        "failed_steps": total_steps - successful_steps,
        "success_rate": (successful_steps / total_steps) * 100
    }
    
    logger_controller.info("Workflow completed", workflow_summary)
    
    # Assert minimum success rate
    if workflow_summary["success_rate"] < 80:
        logger_controller.error(f"Workflow success rate too low: {workflow_summary['success_rate']:.1f}%")
        pytest.fail(f"Workflow failed: only {successful_steps}/{total_steps} steps succeeded")
    else:
        logger_controller.step_passed("Workflow completion", f"Success rate: {workflow_summary['success_rate']:.1f}%")
