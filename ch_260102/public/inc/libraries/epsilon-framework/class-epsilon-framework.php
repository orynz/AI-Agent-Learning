<?php
if ( ! defined( 'WPINC' ) ) {
	die;
}

require_once dirname( __FILE__ ) . '/class-epsilon-autoloader.php';

/**
 * Epsilon Framework
 *
 * @package Epsilon Framework
 */

class Epsilon_Framework {
	/**
	 * Class properties
	 */
	public $controls = array();
	public $sections = array();
	public $path = '';

	/**
	 * Epsilon_Framework constructor.
	 *
	 * @param $args array
	 */
	public function __construct( $args ) {
		foreach ( $args as $k => $v ) {

			if ( ! in_array( $k, array( 'controls', 'sections', 'path' ) ) ) {
				continue;
			}

			$this->$k = $v;
		}

		/**
		 * Customizer enqueues & controls
		 */
		add_action( 'customize_register', array( $this, 'init_controls' ), 0 );

		add_action( 'customize_controls_enqueue_scripts', array( $this, 'customizer_enqueue_scripts' ), 25 );
		add_action( 'customize_preview_init', array( $this, 'customize_preview_styles' ), 25 );

		/**
		 *
		 */
		add_action( 'wp_ajax_epsilon_framework_ajax_action', array(
			$this,
			'epsilon_framework_ajax_action',
		) );

	}

	/**
	 * Init custom controls
	 *
	 * @param object $wp_customize
	 */
	public function init_controls( $wp_customize ) {
		$path = get_template_directory() . $this->path . '/epsilon-framework';

		foreach ( $this->controls as $control ) {
			if ( file_exists( $path . '/controls/class-epsilon-control-' . $control . '.php' ) ) {
				require_once $path . '/controls/class-epsilon-control-' . $control . '.php';
			}
		}

		foreach ( $this->sections as $section ) {
			if ( file_exists( $path . '/sections/class-epsilon-section-' . $section . '.php' ) ) {
				require_once $path . '/sections/class-epsilon-section-' . $section . '.php';
			}
		}
	}

	/**
	 * Binds JS handlers to make Theme Customizer preview reload changes asynchronously.
	 */
	public function customize_preview_styles() {
		wp_enqueue_style( 'epsilon-styles', get_template_directory_uri() . $this->path . '/epsilon-framework/assets/css/style.css' );
		wp_enqueue_script( 'epsilon-previewer', get_template_directory_uri() . $this->path . '/epsilon-framework/assets/js/epsilon-previewer.js', array(
			'jquery',
			'customize-preview',
		), 2, true );

		wp_localize_script( 'epsilon-previewer', 'WPUrls', array(
			'siteurl' => get_option( 'siteurl' ),
			'theme'   => get_template_directory_uri(),
			'ajaxurl' => admin_url( 'admin-ajax.php' ),
		) );
	}

	/*
	 * Our Customizer script
	 *
	 * Dependencies: Customizer Controls script (core)
	 */
	public function customizer_enqueue_scripts() {
		wp_enqueue_script( 'epsilon-object', get_template_directory_uri() . $this->path . '/epsilon-framework/assets/js/epsilon.js', array(
			'jquery',
			'customize-controls',
		) );
		wp_localize_script( 'epsilon-object', 'WPUrls', array(
			'siteurl' => get_option( 'siteurl' ),
			'theme'   => get_template_directory_uri(),
			'ajaxurl' => admin_url( 'admin-ajax.php' ),
			'nonce'   => wp_create_nonce( 'epsilon_framework_ajax_action' ),
		) );
		wp_enqueue_style( 'epsilon-styles', get_template_directory_uri() . $this->path . '/epsilon-framework/assets/css/style.css' );

	}

	/**
	 * Ajax handler
	 */
	public function epsilon_framework_ajax_action() {

		if ( ! check_ajax_referer( 'epsilon_framework_ajax_action', 'security' ) ) {
			wp_die(
				json_encode(
					array(
						'status' => false,
						'error'  => 'Not allowed',
					)
				)
			);
		}

		if ( ! current_user_can( 'manage_options' ) ) {
		    wp_die(
				json_encode(
					array(
						'status' => false,
						'error'  => 'Not allowed',
					)
				)
			);
		}

		if ( ! isset( $_POST['action'] ) || 'epsilon_framework_ajax_action' !== $_POST['action'] ) {
			wp_die(
				json_encode(
					array(
						'status' => false,
						'error'  => 'Not allowed',
					)
				)
			);
		}

		if ( ! isset( $_POST['args'] ) || ! isset( $_POST['args']['action'] ) || ! is_array( $_POST['args']['action'] ) || count( $_POST['args']['action'] ) !== 2 ) {
			wp_die(
				json_encode(
					array(
						'status' => false,
						'error'  => 'Not allowed',
					)
				)
			);
		}

		$class_name = sanitize_text_field( $_POST['args']['action'][0] );
		$method = sanitize_text_field( $_POST['args']['action'][1] );
		
		if ( 'Epsilon_Framework' !== $class_name ) {
			wp_die(
				json_encode(
					array(
						'status' => false,
						'error'  => 'Class does not exist',
					)
				)
			);
		}

		// Only allow specific methods to be called
		$allowed_methods = array( 'dismiss_required_action' );
		if ( ! in_array( $method, $allowed_methods, true ) ) {
			wp_die(
				json_encode(
					array(
						'status' => false,
						'error'  => 'Method not allowed',
					)
				)
			);
		}

		$args = array();
		if ( isset( $_POST['args']['args'] ) ) {
			// Process and sanitize args
			if ( is_array( $_POST['args']['args'] ) ) {
				foreach ( $_POST['args']['args'] as $key => $value ) {
					$args[ sanitize_key( $key ) ] = sanitize_text_field( $value );
				}
			}
		}

		$response = self::$method( $args );

		if ( 'ok' == $response ) {
			wp_die(
				json_encode(
					array(
						'status'  => true,
						'message' => 'ok',
					)
				)
			);
		}

		wp_die(
			json_encode(
				array(
					'status'  => false,
					'message' => 'nok',
				)
			)
		);
	}

	/**
	 * @param $args
	 *
	 * @return string
	 */
	public static function dismiss_required_action( $args ) {
		$option = get_option( $args['option'] );

		if ( $option ) :
			$option[ $args['id'] ] = false;
			update_option( $args['option'], $option );
		else :
			$option = array(
				$args['id'] => false,
			);
			update_option( $args['option'], $option );
		endif;

		return 'ok';
	}
}
